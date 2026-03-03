"""
Regra de Pedágio 50% (Transição)
Base legal: Art. 17 da EC 103/2019
"""

from datetime import date, timedelta
from app.core.rules import RegraBase, ResultadoRegra
from app.models.cliente import Cliente

class RegraPedagio50(RegraBase):
    """
    Regra de Aposentadoria com Pedágio de 50% (Transição)
    """
    
    def __init__(self):
        self.data_corte = date(2019, 11, 13)
    
    def nome(self) -> str:
        return "Pedágio 50% (Transição)"
    
    def _arredondar(self, valor: float, casas: int = 2) -> float:
        """Arredonda valor para o número especificado de casas decimais"""
        return round(valor, casas)
    
    def _calcular_tempo_faltante_em_2019(self, cliente: Cliente) -> float:
        """
        Calcula quanto tempo faltava para o cliente se aposentar em 13/11/2019
        """
        tempo_necessario = 35 if cliente.sexo == "M" else 30
        
        if not cliente.data_filiacao_rgps:
            return 0
        
        dias_ate_corte = (self.data_corte - cliente.data_filiacao_rgps).days
        tempo_ate_corte = max(0, dias_ate_corte / 365.25)
        
        return self._arredondar(max(0, tempo_necessario - tempo_ate_corte))
    
    def verificar(self, cliente: Cliente) -> ResultadoRegra:
        """
        Verifica elegibilidade para Pedágio 50%
        """
        if not cliente.elegivel_transicao:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Cliente não tem direito às regras de transição",
                detalhes={"motivo": "pos_reforma"}
            )
        
        tempo_faltante_2019 = self._calcular_tempo_faltante_em_2019(cliente)
        
        if tempo_faltante_2019 > 2.1:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta=f"Em 13/11/2019 faltavam {tempo_faltante_2019:.2f} anos (> 2 anos)",
                detalhes={
                    "tempo_faltante_2019": tempo_faltante_2019,
                    "motivo": "tempo_faltante_superior_2anos"
                }
            )
        
        pedagio = self._arredondar(tempo_faltante_2019 * 0.5)
        tempo_a_cumprir = self._arredondar(tempo_faltante_2019 + pedagio)
        
        dias_apos_corte = (date.today() - self.data_corte).days
        tempo_apos_corte = self._arredondar(max(0, dias_apos_corte / 365.25))
        
        elegivel = tempo_apos_corte >= tempo_a_cumprir - 0.1
        
        if elegivel:
            rmi_estimada = None
            if cliente.salarios_contribuicao:
                salarios_ordenados = sorted(cliente.salarios_contribuicao, reverse=True)
                n = len(salarios_ordenados)
                k = int(n * 0.8)
                maiores_80 = salarios_ordenados[:k]
                media_80 = sum(maiores_80) / len(maiores_80) if maiores_80 else 0
                
                idade = self._arredondar(cliente.idade_exata if hasattr(cliente, 'idade_exata') else cliente.idade)
                
                expectativa = 18.2
                fator = (tempo_a_cumprir * 0.31 / expectativa) * (1 + (idade + tempo_a_cumprir * 0.31) / 100)
                fator = max(1.0, self._arredondar(fator, 4))
                
                rmi_estimada = self._arredondar(media_80 * fator)
            
            o_que_falta = None
            detalhes = {
                "tempo_faltante_2019": tempo_faltante_2019,
                "pedagio_50": pedagio,
                "tempo_a_cumprir": tempo_a_cumprir,
                "tempo_apos_corte": tempo_apos_corte,
                "fator_previdenciario": fator
            }
        else:
            tempo_restante = self._arredondar(tempo_a_cumprir - tempo_apos_corte)
            o_que_falta = f"Faltam {tempo_restante:.2f} anos para cumprir pedágio de 50%"
            detalhes = {
                "tempo_faltante_2019": tempo_faltante_2019,
                "pedagio_50": pedagio,
                "tempo_a_cumprir": tempo_a_cumprir,
                "tempo_ja_cumprido": tempo_apos_corte
            }
            rmi_estimada = None
        
        return ResultadoRegra(
            nome_regra=self.nome(),
            elegivel=elegivel,
            rmi_estimada=rmi_estimada,
            o_que_falta=o_que_falta,
            detalhes=detalhes
        )
