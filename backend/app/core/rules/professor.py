"""
Regra de Aposentadoria para Professor
Base legal: Art. 201 da Constituição Federal
- Redução de 5 anos nos requisitos
- Exclusivo para ensino infantil, fundamental e médio
"""

from datetime import date
from app.core.rules import RegraBase, ResultadoRegra
from app.models.cliente import Cliente

class RegraProfessor(RegraBase):
    """
    Regra de Aposentadoria para Professor
    """
    
    def __init__(self):
        self.requisitos = {
            "M": {
                "tempo_contribuicao": 30,  # 35 - 5
                "idade_minima": 60,         # 65 - 5
                "pedagio_idade": 55,        # Para pedágio 100%
                "pontos_base": 88            # Para regra de pontos (ajustado)
            },
            "F": {
                "tempo_contribuicao": 25,   # 30 - 5
                "idade_minima": 57,          # 62 - 5
                "pedagio_idade": 52,         # Para pedágio 100%
                "pontos_base": 83            # Para regra de pontos (ajustado)
            }
        }
    
    def nome(self) -> str:
        return "Aposentadoria de Professor (Especial)"
    
    def _arredondar(self, valor: float, casas: int = 2) -> float:
        return round(valor, casas)
    
    def verificar(self, cliente: Cliente) -> ResultadoRegra:
        """
        Verifica elegibilidade para Aposentadoria de Professor
        """
        if not cliente.professor:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Cliente não é professor",
                detalhes={"motivo": "nao_professor"}
            )
        
        req = self.requisitos.get(cliente.sexo)
        if not req:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Sexo não especificado",
                detalhes={"erro": "sexo_invalido"}
            )
        
        # Verificar tempo de contribuição
        tempo_contribuicao_anos = cliente.tempo_contribuicao_dias / 365.25
        tempo_ok = tempo_contribuicao_anos >= req["tempo_contribuicao"] - 0.01
        
        # Verificar idade
        idade_ok = cliente.idade >= req["idade_minima"] - 0.01
        
        # Verificar se tem direito adquirido (pré-reforma)
        direito_adquirido = False
        if cliente.data_filiacao_rgps and cliente.data_filiacao_rgps < date(2019, 11, 13):
            if tempo_contribuicao_anos >= req["tempo_contribuicao"]:
                direito_adquirido = True
        
        elegivel = (direito_adquirido or (idade_ok and tempo_ok))
        
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
            detalhes = {
                "tempo_contribuicao": self._arredondar(tempo_contribuicao_anos),
                "tempo_necessario": req["tempo_contribuicao"],
                "idade_atual": cliente.idade,
                "idade_minima": req["idade_minima"],
                "direito_adquirido": direito_adquirido
            }
        else:
            faltas = []
            if not tempo_ok:
                anos_faltando = req["tempo_contribuicao"] - tempo_contribuicao_anos
                faltas.append(f"{self._arredondar(anos_faltando)} anos de contribuição")
            if not idade_ok and not direito_adquirido:
                anos_faltando = req["idade_minima"] - cliente.idade
                faltas.append(f"{self._arredondar(anos_faltando)} anos de idade")
            
            o_que_falta = "Falta: " + ", ".join(faltas)
            rmi_estimada = None
            detalhes = {
                "tempo_contribuicao": self._arredondar(tempo_contribuicao_anos),
                "tempo_necessario": req["tempo_contribuicao"],
                "idade_atual": cliente.idade,
                "idade_minima": req["idade_minima"]
            }
        
        return ResultadoRegra(
            nome_regra=self.nome(),
            elegivel=elegivel,
            rmi_estimada=rmi_estimada,
            o_que_falta=o_que_falta,
            detalhes=detalhes
        )
