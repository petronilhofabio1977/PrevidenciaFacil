"""
Regra de Aposentadoria para Pessoa com Deficiência
Base legal: Lei Complementar 142/2013
Graus:
- Grave: 25 anos (H) / 20 anos (M)
- Moderada: 29 anos (H) / 24 anos (M)
- Leve: 33 anos (H) / 28 anos (M)
"""

from datetime import date
from app.core.rules import RegraBase, ResultadoRegra
from app.models.cliente import Cliente

class RegraDeficiente(RegraBase):
    """
    Regra de Aposentadoria para Pessoa com Deficiência
    """
    
    def __init__(self):
        self.tempo_por_grau = {
            "grave": {"M": 25, "F": 20},
            "moderada": {"M": 29, "F": 24},
            "leve": {"M": 33, "F": 28}
        }
        self.idade_por_grau = {
            "grave": {"M": 55, "F": 50},  # Por idade
            "moderada": {"M": 58, "F": 53},
            "leve": {"M": 60, "F": 55}
        }
    
    def nome(self) -> str:
        return "Aposentadoria da Pessoa com Deficiência"
    
    def _arredondar(self, valor: float, casas: int = 2) -> float:
        return round(valor, casas)
    
    def verificar(self, cliente: Cliente) -> ResultadoRegra:
        """
        Verifica elegibilidade para Aposentadoria de Deficiente
        """
        if cliente.deficiencia == "nenhuma":
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Cliente não possui deficiência",
                detalhes={"motivo": "sem_deficiencia"}
            )
        
        grau = cliente.deficiencia.lower()
        if grau not in self.tempo_por_grau:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta=f"Grau de deficiência não reconhecido: {grau}",
                detalhes={"grau": grau}
            )
        
        tempo_contribuicao_anos = cliente.tempo_contribuicao_dias / 365.25
        tempo_necessario = self.tempo_por_grau[grau][cliente.sexo]
        
        # Verificar por tempo
        elegivel_tempo = tempo_contribuicao_anos >= tempo_necessario - 0.01
        
        # Verificar por idade (alternativa)
        idade_necessaria = self.idade_por_grau[grau][cliente.sexo]
        elegivel_idade = cliente.idade >= idade_necessaria and tempo_contribuicao_anos >= 15
        
        elegivel = elegivel_tempo or elegivel_idade
        
        if elegivel:
            # Calcular RMI
            rmi_estimada = None
            if cliente.salarios_contribuicao:
                salarios_ordenados = sorted(cliente.salarios_contribuicao, reverse=True)
                n = len(salarios_ordenados)
                k = int(n * 0.8)
                maiores_80 = salarios_ordenados[:k]
                rmi_estimada = self._arredondar(sum(maiores_80) / len(maiores_80) if maiores_80 else 0)
            
            o_que_falta = None
            tipo = "por tempo" if elegivel_tempo else "por idade"
            detalhes = {
                "grau": grau,
                "tipo_aposentadoria": tipo,
                "tempo_contribuicao": self._arredondar(tempo_contribuicao_anos),
                "tempo_necessario": tempo_necessario,
                "idade_atual": cliente.idade,
                "idade_necessaria": idade_necessaria
            }
        else:
            faltas = []
            if not elegivel_tempo:
                anos_faltando = tempo_necessario - tempo_contribuicao_anos
                faltas.append(f"{self._arredondar(anos_faltando)} anos de contribuição (deficiência {grau})")
            if not elegivel_idade and cliente.idade < idade_necessaria:
                anos_faltando = idade_necessaria - cliente.idade
                faltas.append(f"{self._arredondar(anos_faltando)} anos de idade (deficiência {grau})")
            
            o_que_falta = "Falta: " + ", ".join(faltas)
            rmi_estimada = None
            detalhes = {
                "grau": grau,
                "tempo_contribuicao": self._arredondar(tempo_contribuicao_anos),
                "tempo_necessario": tempo_necessario,
                "idade_atual": cliente.idade,
                "idade_necessaria": idade_necessaria
            }
        
        return ResultadoRegra(
            nome_regra=self.nome(),
            elegivel=elegivel,
            rmi_estimada=rmi_estimada,
            o_que_falta=o_que_falta,
            detalhes=detalhes
        )
