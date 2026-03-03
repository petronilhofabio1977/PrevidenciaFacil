from typing import List, Optional
from datetime import date
import logging
from app.models.cliente import ClienteDB as Cliente
from app.core.rules import RegraBase, ResultadoRegra
from app.core.rules.pontos import RegraPontos
from app.core.rules.pedagio_50 import RegraPedagio50
from app.core.rules.pedagio_100 import RegraPedagio100
from app.core.rules.idade import RegraIdade
from app.core.rules.transicao_idade import RegraTransicaoIdade
from app.core.rules.direito_adquirido import RegraDireitoAdquirido
from app.core.rules.especial import RegraEspecial
from app.core.rules.professor import RegraProfessor
from app.core.rules.rural import RegraRural
from app.core.rules.deficiente import RegraDeficiente

logger = logging.getLogger(__name__)


class MotorPrevidenciario:
    """
    Orquestrador de todas as regras previdenciárias.

    Ordem das regras importa: DireitoAdquirido tem prioridade absoluta.
    As demais são avaliadas independentemente e ranqueadas por vantagem.
    """

    # Regras que, se elegíveis, encerram a análise imediatamente
    REGRAS_PRIORITARIAS = {"Direito Adquirido"}

    def __init__(self):
        self.regras: List[RegraBase] = [
            RegraDireitoAdquirido(),     # 1. Prioridade absoluta
            RegraPontos(),               # 2. Regra de Pontos
            RegraPedagio50(),            # 3. Pedágio 50%
            RegraPedagio100(),           # 4. Pedágio 100%
            RegraIdade(),                # 5. Aposentadoria por Idade
            RegraTransicaoIdade(),       # 6. Transição por Idade
            RegraEspecial(),             # 7. Aposentadoria Especial
            RegraProfessor(),            # 8. Professor
            RegraRural(),                # 9. Rural
            RegraDeficiente(),           # 10. Pessoa com Deficiência
        ]

    # ------------------------------------------------------------------
    # Análise
    # ------------------------------------------------------------------

    def analisar(self, cliente: Cliente) -> List[ResultadoRegra]:
        """
        Executa todas as regras para o cliente.

        Interrompe antecipadamente se uma regra prioritária for elegível
        (ex.: Direito Adquirido — não há nada melhor a comparar).
        """
        resultados: List[ResultadoRegra] = []

        for regra in self.regras:
            resultado = self._executar_regra(regra, cliente)
            resultados.append(resultado)

            if resultado.elegivel and regra.nome() in self.REGRAS_PRIORITARIAS:
                logger.info(
                    "Regra prioritária '%s' elegível para %s — análise encerrada.",
                    regra.nome(), cliente.cpf,
                )
                break

        return resultados

    def _executar_regra(self, regra: RegraBase, cliente: Cliente) -> ResultadoRegra:
        """Executa uma única regra com tratamento de erro isolado."""
        try:
            return regra.verificar(cliente)
        except Exception as exc:  # noqa: BLE001
            logger.exception(
                "Erro inesperado na regra '%s' para CPF %s: %s",
                regra.nome(), cliente.cpf, exc,
            )
            return ResultadoRegra(
                nome_regra=regra.nome(),
                elegivel=False,
                o_que_falta="Erro interno na verificação desta regra.",
                detalhes={"erro": True, "mensagem": str(exc)},
            )

    # ------------------------------------------------------------------
    # Seleção da melhor opção
    # ------------------------------------------------------------------

    def mais_vantajoso(self, resultados: List[ResultadoRegra]) -> Optional[ResultadoRegra]:
        """
        Retorna a regra elegível mais vantajosa.

        Critério primário  : maior RMI estimada.
        Critério secundário: menor tempo faltando (meses_faltando, se disponível),
                             útil quando duas regras têm RMI idêntica ou nula.
        """
        elegiveis = [r for r in resultados if r.elegivel]
        if not elegiveis:
            return None

        def _chave(r: ResultadoRegra):
            rmi = r.rmi_estimada or 0.0
            # Menor prazo = melhor: invertemos o sinal para usar max()
            meses = -(r.detalhes.get("meses_faltando") or 0)
            return (rmi, meses)

        return max(elegiveis, key=_chave)

    def mais_proximo(self, resultados: List[ResultadoRegra]) -> Optional[ResultadoRegra]:
        """
        Entre os NÃO elegíveis, retorna o mais próximo de se tornar elegível
        (menor meses_faltando nos detalhes).
        """
        nao_elegiveis = [
            r for r in resultados
            if not r.elegivel and isinstance(r.detalhes.get("meses_faltando"), (int, float))
        ]
        if not nao_elegiveis:
            return None
        return min(nao_elegiveis, key=lambda r: r.detalhes["meses_faltando"])

    # ------------------------------------------------------------------
    # Recomendação completa
    # ------------------------------------------------------------------

    def recomendar(self, cliente: Cliente) -> dict:
        """
        Executa análise completa e devolve um dict pronto para serialização
        (FastAPI, JSON, etc.).
        """
        resultados = self.analisar(cliente)
        melhor = self.mais_vantajoso(resultados)
        proximo = self.mais_proximo(resultados) if not melhor else None

        return {
            "cliente": cliente.nome_completo,
            "cpf": cliente.cpf,
            "data_analise": date.today().isoformat(),
            "resultados": [self._serializar_resultado(r) for r in resultados],
            **self._montar_recomendacao(melhor, proximo),
        }

    # ------------------------------------------------------------------
    # Helpers privados
    # ------------------------------------------------------------------

    @staticmethod
    def _serializar_resultado(r: ResultadoRegra) -> dict:
        return {
            "nome_regra": r.nome_regra,
            "elegivel": r.elegivel,
            "rmi_estimada": r.rmi_estimada,
            "o_que_falta": r.o_que_falta,
            "detalhes": r.detalhes,
        }

    @staticmethod
    def _montar_recomendacao(
        melhor: Optional[ResultadoRegra],
        proximo: Optional[ResultadoRegra],
    ) -> dict:
        if melhor:
            rmi_txt = (
                f"R$ {melhor.rmi_estimada:.2f}"
                if melhor.rmi_estimada is not None
                else "a calcular"
            )
            return {
                "recomendacao": melhor.nome_regra,
                "motivo_recomendacao": f"Maior RMI estimada: {rmi_txt}",
                "proximo_beneficio": None,
            }

        proximo_info = None
        if proximo:
            meses = proximo.detalhes.get("meses_faltando")
            proximo_info = {
                "nome_regra": proximo.nome_regra,
                "meses_faltando": meses,
            }

        return {
            "recomendacao": None,
            "motivo_recomendacao": "Nenhuma regra elegível no momento.",
            "proximo_beneficio": proximo_info,
        }