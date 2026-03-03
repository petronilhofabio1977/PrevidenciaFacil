"""
Regra de Aposentadoria por Idade (Regra Permanente)
Base legal: Art. 19 da EC 103/2019
"""

from datetime import date
from app.core.rules import RegraBase, ResultadoRegra
from app.models.cliente import Cliente

class RegraIdade(RegraBase):
    """
    Regra de Aposentadoria por Idade (Permanente)
    """
    
    def __init__(self):
        self.requisitos = {
            "M": {
                "idade_minima": 65,
                "tempo_minimo_anos": 20,
                "carencia_meses": 180
            },
            "F": {
                "idade_minima": 62,
                "tempo_minimo_anos": 15,
                "carencia_meses": 180
            }
        }
    
    def nome(self) -> str:
        return "Aposentadoria por Idade (Permanente)"
    
    def _arredondar(self, valor: float, casas: int = 2) -> float:
        """Arredonda valor para o número especificado de casas decimais"""
        return round(valor, casas)
    
    def _calcular_idade_exata(self, data_nascimento: date) -> float:
        """Calcula idade exata em anos (com decimal)"""
        hoje = date.today()
        idade = hoje.year - data_nascimento.year
        
        if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        
        dia_aniversario = date(hoje.year, data_nascimento.month, data_nascimento.day)
        if hoje < dia_aniversario:
            dia_aniversario = date(hoje.year - 1, data_nascimento.month, data_nascimento.day)
        
        dias_desde_aniversario = (hoje - dia_aniversario).days
        return self._arredondar(idade + (dias_desde_aniversario / 365.25))
    
    def verificar(self, cliente: Cliente) -> ResultadoRegra:
        """
        Verifica elegibilidade para Aposentadoria por Idade
        """
        req = self.requisitos.get(cliente.sexo)
        if not req:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Sexo não especificado corretamente",
                detalhes={"erro": "sexo_invalido"}
            )
        
        idade_exata = self._calcular_idade_exata(cliente.data_nascimento)
        tempo_contribuicao_anos = self._arredondar(cliente.tempo_contribuicao_dias / 365.25)
        meses_contribuicao = len(cliente.salarios_contribuicao) if cliente.salarios_contribuicao else 0
        
        idade_ok = idade_exata >= req["idade_minima"] - 0.01
        tempo_ok = tempo_contribuicao_anos >= req["tempo_minimo_anos"] - 0.01
        carencia_ok = meses_contribuicao >= req["carencia_meses"]
        
        elegivel = idade_ok and tempo_ok and carencia_ok
        
        if elegivel:
            rmi_estimada = None
            if cliente.salarios_contribuicao:
                salarios_ordenados = sorted(cliente.salarios_contribuicao, reverse=True)
                n = len(salarios_ordenados)
                k = int(n * 0.8)
                maiores_80 = salarios_ordenados[:k]
                media_80 = sum(maiores_80) / len(maiores_80) if maiores_80 else 0
                
                anos_base = 20 if cliente.sexo == "M" else 15
                anos_extras = max(0, int(tempo_contribuicao_anos - anos_base))
                coeficiente = min(100, 70 + anos_extras)
                
                rmi_estimada = self._arredondar(media_80 * (coeficiente / 100))
            
            o_que_falta = None
            detalhes = {
                "idade_atual": idade_exata,
                "idade_necessaria": req["idade_minima"],
                "tempo_atual": tempo_contribuicao_anos,
                "tempo_necessario": req["tempo_minimo_anos"],
                "coeficiente": f"{coeficiente}%"
            }
        else:
            faltas = []
            if not idade_ok:
                anos_faltando = self._arredondar(req["idade_minima"] - idade_exata)
                faltas.append(f"{anos_faltando:.2f} anos de idade")
            if not tempo_ok:
                anos_faltando = self._arredondar(req["tempo_minimo_anos"] - tempo_contribuicao_anos)
                faltas.append(f"{anos_faltando:.2f} anos de contribuição")
            if not carencia_ok:
                faltas.append(f"{req['carencia_meses'] - meses_contribuicao} meses de carência")
            
            o_que_falta = "Falta: " + ", ".join(faltas)
            rmi_estimada = None
            detalhes = {
                "idade_atual": idade_exata,
                "idade_necessaria": req["idade_minima"],
                "tempo_atual": tempo_contribuicao_anos,
                "tempo_necessario": req["tempo_minimo_anos"],
                "carencia_ok": carencia_ok
            }
        
        return ResultadoRegra(
            nome_regra=self.nome(),
            elegivel=elegivel,
            rmi_estimada=rmi_estimada,
            o_que_falta=o_que_falta,
            detalhes=detalhes
        )
