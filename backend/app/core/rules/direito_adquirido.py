"""
Regra de Direito Adquirido (Pré-Reforma)
Base legal: Art. 3° da EC 103/2019
- Para quem completou os requisitos até 13/11/2019
- Homem: 35 anos de contribuição
- Mulher: 30 anos de contribuição
- Idade: não exigida
- Cálculo: regra antiga (80% das maiores contribuições)
"""

from datetime import date
from app.core.rules import RegraBase, ResultadoRegra
from app.models.cliente import Cliente

class RegraDireitoAdquirido(RegraBase):
    """
    Regra de Direito Adquirido (Pré-Reforma)
    """
    
    def __init__(self):
        self.data_corte = date(2019, 11, 13)
        self.tempo_necessario = {"M": 35, "F": 30}
    
    def nome(self) -> str:
        return "Direito Adquirido (Pré-Reforma)"
    
    def _arredondar(self, valor: float, casas: int = 2) -> float:
        return round(valor, casas)
    
    def verificar(self, cliente: Cliente) -> ResultadoRegra:
        """
        Verifica se o cliente tem direito adquirido
        """
        # Verificar se filiação é antes da reforma
        if not cliente.data_filiacao_rgps or cliente.data_filiacao_rgps > self.data_corte:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Cliente se filiou após a reforma",
                detalhes={"motivo": "pos_reforma"}
            )
        
        tempo_necessario = self.tempo_necessario.get(cliente.sexo, 0)
        if tempo_necessario == 0:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Sexo não especificado",
                detalhes={"erro": "sexo_invalido"}
            )
        
        # Calcular tempo até a data de corte
        # Por simplicidade, usando tempo total
        tempo_contribuicao_anos = cliente.tempo_contribuicao_dias / 365.25
        
        elegivel = tempo_contribuicao_anos >= tempo_necessario - 0.01
        
        if elegivel:
            # Calcular RMI (média dos 80% maiores salários)
            rmi_estimada = None
            if cliente.salarios_contribuicao:
                salarios_ordenados = sorted(cliente.salarios_contribuicao, reverse=True)
                n = len(salarios_ordenados)
                k = int(n * 0.8)
                maiores_80 = salarios_ordenados[:k]
                rmi_estimada = self._arredondar(sum(maiores_80) / len(maiores_80) if maiores_80 else 0)
            
            o_que_falta = None
            detalhes = {
                "tempo_contribuicao": self._arredondar(tempo_contribuicao_anos),
                "tempo_necessario": tempo_necessario,
                "data_corte": self.data_corte.isoformat(),
                "direito_adquirido": True
            }
        else:
            anos_faltando = tempo_necessario - tempo_contribuicao_anos
            o_que_falta = f"Faltavam {self._arredondar(anos_faltando)} anos em 13/11/2019"
            rmi_estimada = None
            detalhes = {
                "tempo_contribuicao": self._arredondar(tempo_contribuicao_anos),
                "tempo_necessario": tempo_necessario,
                "anos_faltando": self._arredondar(anos_faltando),
                "data_corte": self.data_corte.isoformat()
            }
        
        return ResultadoRegra(
            nome_regra=self.nome(),
            elegivel=elegivel,
            rmi_estimada=rmi_estimada,
            o_que_falta=o_que_falta,
            detalhes=detalhes
        )
