"""
Regra de Aposentadoria Rural (Segurado Especial)
Base legal: Art. 48 da Lei 8.213/1991
- Idade: 60 anos (H) / 55 anos (M)
- Carência: 15 anos de atividade rural
- Não exige tempo de contribuição urbano
"""

from datetime import date
from app.core.rules import RegraBase, ResultadoRegra
from app.models.cliente import Cliente

class RegraRural(RegraBase):
    """
    Regra de Aposentadoria Rural (Segurado Especial)
    """
    
    def __init__(self):
        self.requisitos = {
            "M": {"idade_minima": 60, "tempo_atividade": 15},
            "F": {"idade_minima": 55, "tempo_atividade": 15}
        }
    
    def nome(self) -> str:
        return "Aposentadoria Rural (Segurado Especial)"
    
    def _arredondar(self, valor: float, casas: int = 2) -> float:
        return round(valor, casas)
    
    def verificar(self, cliente: Cliente) -> ResultadoRegra:
        """
        Verifica elegibilidade para Aposentadoria Rural
        """
        if not cliente.atividade_rural:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Cliente não é segurado especial rural",
                detalhes={"motivo": "nao_rural"}
            )
        
        req = self.requisitos.get(cliente.sexo)
        if not req:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Sexo não especificado",
                detalhes={"erro": "sexo_invalido"}
            )
        
        # Verificar idade
        idade_ok = cliente.idade >= req["idade_minima"]
        
        # Para atividade rural, consideramos o tempo total como aproximação
        # Idealmente, teríamos um campo específico para tempo de atividade rural
        tempo_rural_anos = cliente.tempo_contribuicao_dias / 365.25
        tempo_ok = tempo_rural_anos >= req["tempo_atividade"] - 0.01
        
        elegivel = idade_ok and tempo_ok
        
        if elegivel:
            # Calcular RMI (75% do salário mínimo para rurais)
            # Usando valor aproximado do salário mínimo 2026
            salario_minimo = 1518.00  # Aproximado
            rmi_estimada = self._arredondar(salario_minimo * 0.75)
            
            o_que_falta = None
            detalhes = {
                "idade_atual": cliente.idade,
                "idade_minima": req["idade_minima"],
                "tempo_atividade": self._arredondar(tempo_rural_anos),
                "tempo_necessario": req["tempo_atividade"],
                "salario_minimo": salario_minimo
            }
        else:
            faltas = []
            if not idade_ok:
                faltas.append(f"{req['idade_minima'] - cliente.idade} anos de idade")
            if not tempo_ok:
                anos_faltando = req["tempo_atividade"] - tempo_rural_anos
                faltas.append(f"{self._arredondar(anos_faltando)} anos de atividade rural")
            
            o_que_falta = "Falta: " + ", ".join(faltas)
            rmi_estimada = None
            detalhes = {
                "idade_atual": cliente.idade,
                "idade_minima": req["idade_minima"],
                "tempo_atividade": self._arredondar(tempo_rural_anos),
                "tempo_necessario": req["tempo_atividade"]
            }
        
        return ResultadoRegra(
            nome_regra=self.nome(),
            elegivel=elegivel,
            rmi_estimada=rmi_estimada,
            o_que_falta=o_que_falta,
            detalhes=detalhes
        )
