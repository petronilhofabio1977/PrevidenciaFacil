"""
Regra de Aposentadoria Especial
Base legal: Art. 57 da Lei 8.213/1991
- Trabalho com agentes nocivos
- 15, 20 ou 25 anos conforme o risco
- Regra de transição: pontos (66/76/86) + idade
- Regra nova: idade mínima (55/58/60)
"""

from datetime import date
from app.core.rules import RegraBase, ResultadoRegra
from app.models.cliente import Cliente

class RegraEspecial(RegraBase):
    """
    Regra de Aposentadoria Especial
    """
    
    def __init__(self):
        self.tempo_por_risco = {
            "15": 15,   # Risco muito alto
            "20": 20,   # Risco alto
            "25": 25    # Risco moderado
        }
        self.idade_nova = {
            "15": 55,
            "20": 58,
            "25": 60
        }
        self.pontos_transicao = {
            "15": 66,
            "20": 76,
            "25": 86
        }
    
    def nome(self) -> str:
        return "Aposentadoria Especial"
    
    def _arredondar(self, valor: float, casas: int = 2) -> float:
        return round(valor, casas)
    
    def _determinar_risco(self, cliente: Cliente) -> tuple:
        """
        Determina o grau de risco baseado nos períodos especiais
        Retorna (anos_especiais, categoria_risco)
        """
        # Simplificação: se tem atividade especial, considera 25 anos
        # Idealmente, analisaria os agentes nocivos
        if cliente.tem_atividade_especial:
            return 25, "25"
        return 0, None
    
    def verificar(self, cliente: Cliente) -> ResultadoRegra:
        """
        Verifica elegibilidade para Aposentadoria Especial
        """
        anos_especiais, risco = self._determinar_risco(cliente)
        
        if not risco:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Cliente não possui atividade especial",
                detalhes={"motivo": "sem_especial"}
            )
        
        tempo_necessario = self.tempo_por_risco[risco]
        
        # Direito adquirido (pré-reforma)
        if cliente.data_filiacao_rgps and cliente.data_filiacao_rgps < date(2019, 11, 13):
            if anos_especiais >= tempo_necessario - 0.01:
                # Direito adquirido
                rmi_estimada = None
                if cliente.salarios_contribuicao:
                    salarios_ordenados = sorted(cliente.salarios_contribuicao, reverse=True)
                    n = len(salarios_ordenados)
                    k = int(n * 0.8)
                    maiores_80 = salarios_ordenados[:k]
                    rmi_estimada = self._arredondar(sum(maiores_80) / len(maiores_80) if maiores_80 else 0)
                
                return ResultadoRegra(
                    nome_regra=self.nome(),
                    elegivel=True,
                    rmi_estimada=rmi_estimada,
                    o_que_falta=None,
                    detalhes={
                        "tipo": "direito_adquirido",
                        "tempo_especial": self._arredondar(anos_especiais),
                        "tempo_necessario": tempo_necessario
                    }
                )
        
        # Regra de transição (pontos + idade)
        pontos_necessarios = self.pontos_transicao[risco]
        idade = cliente.idade_exata
        pontos = idade + anos_especiais
        
        elegivel_transicao = pontos >= pontos_necessarios - 0.01
        
        # Regra nova (idade mínima)
        idade_necessaria = self.idade_nova[risco]
        elegivel_nova = idade >= idade_necessaria - 0.01 and anos_especiais >= tempo_necessario - 0.01
        
        elegivel = elegivel_transicao or elegivel_nova
        
        if elegivel:
            rmi_estimada = None
            if cliente.salarios_contribuicao:
                salarios_ordenados = sorted(cliente.salarios_contribuicao, reverse=True)
                n = len(salarios_ordenados)
                k = int(n * 0.8)
                maiores_80 = salarios_ordenados[:k]
                rmi_estimada = self._arredondar(sum(maiores_80) / len(maiores_80) if maiores_80 else 0)
            
            o_que_falta = None
            tipo = "transicao" if elegivel_transicao else "nova_regra"
            detalhes = {
                "tipo": tipo,
                "risco": risco,
                "tempo_especial": self._arredondar(anos_especiais),
                "tempo_necessario": tempo_necessario,
                "idade_atual": idade,
                "pontos_atuais": self._arredondar(pontos),
                "pontos_necessarios": pontos_necessarios if elegivel_transicao else None,
                "idade_necessaria": idade_necessaria if elegivel_nova else None
            }
        else:
            faltas = []
            if anos_especiais < tempo_necessario - 0.01:
                anos_faltando = tempo_necessario - anos_especiais
                faltas.append(f"{self._arredondar(anos_faltando)} anos de atividade especial")
            if not elegivel_transicao and not elegivel_nova:
                if pontos < pontos_necessarios:
                    pontos_faltando = pontos_necessarios - pontos
                    faltas.append(f"{self._arredondar(pontos_faltando)} pontos (regra transição)")
                if idade < idade_necessaria:
                    anos_faltando = idade_necessaria - idade
                    faltas.append(f"{self._arredondar(anos_faltando)} anos de idade (nova regra)")
            
            o_que_falta = "Falta: " + ", ".join(faltas)
            rmi_estimada = None
            detalhes = {
                "risco": risco,
                "tempo_especial": self._arredondar(anos_especiais),
                "tempo_necessario": tempo_necessario,
                "idade_atual": idade,
                "pontos_atuais": self._arredondar(pontos),
                "pontos_necessarios": pontos_necessarios
            }
        
        return ResultadoRegra(
            nome_regra=self.nome(),
            elegivel=elegivel,
            rmi_estimada=rmi_estimada,
            o_que_falta=o_que_falta,
            detalhes=detalhes
        )
