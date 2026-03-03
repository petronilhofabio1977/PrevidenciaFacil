"""
Regra de Pedágio 100% (Transição)
Base legal: Art. 20 da EC 103/2019
- Idade mínima: 60 anos (H) / 57 anos (M)
- Tempo de contribuição: 35 anos (H) / 30 anos (M)
- Cumprir 100% do tempo que faltava em 13/11/2019
- Recebe 100% da média salarial
"""

from datetime import date, timedelta
from app.core.rules import RegraBase, ResultadoRegra
from app.models.cliente import Cliente

class RegraPedagio100(RegraBase):
    """
    Regra de Aposentadoria com Pedágio de 100% (Transição)
    """
    
    def __init__(self):
        self.data_corte = date(2019, 11, 13)
        self.requisitos = {
            "M": {"idade_minima": 60, "tempo_necessario": 35},
            "F": {"idade_minima": 57, "tempo_necessario": 30}
        }
    
    def nome(self) -> str:
        return "Pedágio 100% (Transição)"
    
    def _arredondar(self, valor: float, casas: int = 2) -> float:
        return round(valor, casas)
    
    def _calcular_tempo_faltante_2019(self, cliente: Cliente) -> float:
        """Calcula quanto tempo faltava em 13/11/2019"""
        req = self.requisitos.get(cliente.sexo)
        if not req:
            return 0
        
        # Calcular tempo até a data de corte
        if not cliente.data_filiacao_rgps:
            return req["tempo_necessario"]
        
        dias_ate_corte = (self.data_corte - cliente.data_filiacao_rgps).days
        tempo_ate_corte = max(0, dias_ate_corte / 365.25)
        
        return max(0, req["tempo_necessario"] - tempo_ate_corte)
    
    def verificar(self, cliente: Cliente) -> ResultadoRegra:
        """
        Verifica elegibilidade para Pedágio 100%
        """
        if not cliente.elegivel_transicao:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Cliente não tem direito às regras de transição",
                detalhes={"motivo": "pos_reforma"}
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
        
        # Calcular tempo faltante em 2019
        tempo_faltante_2019 = self._calcular_tempo_faltante_2019(cliente)
        
        # Tempo que ele precisava cumprir (100% do que faltava)
        tempo_a_cumprir = tempo_faltante_2019 * 2  # 100% = dobro
        
        # Tempo que ele já contribuiu após a reforma
        dias_apos_corte = (date.today() - self.data_corte).days
        tempo_apos_corte = max(0, dias_apos_corte / 365.25)
        
        # Verificar se já cumpriu
        tempo_ok = tempo_apos_corte >= tempo_a_cumprir - 0.01
        
        elegivel = idade_ok and tempo_ok
        
        if elegivel:
            # Calcular RMI (100% da média)
            rmi_estimada = None
            if cliente.salarios_contribuicao:
                salarios_ordenados = sorted(cliente.salarios_contribuicao, reverse=True)
                n = len(salarios_ordenados)
                k = int(n * 0.8)
                maiores_80 = salarios_ordenados[:k]
                rmi_estimada = self._arredondar(sum(maiores_80) / len(maiores_80) if maiores_80 else 0)
            
            o_que_falta = None
            detalhes = {
                "idade_atual": cliente.idade,
                "idade_minima": req["idade_minima"],
                "tempo_faltante_2019": self._arredondar(tempo_faltante_2019),
                "tempo_a_cumprir": self._arredondar(tempo_a_cumprir),
                "tempo_ja_cumprido": self._arredondar(tempo_apos_corte)
            }
        else:
            faltas = []
            if not idade_ok:
                faltas.append(f"{req['idade_minima'] - cliente.idade} anos de idade")
            if not tempo_ok:
                anos_faltando = self._arredondar(tempo_a_cumprir - tempo_apos_corte)
                faltas.append(f"{anos_faltando} anos de contribuição (pedágio 100%)")
            
            o_que_falta = "Falta: " + ", ".join(faltas)
            rmi_estimada = None
            detalhes = {
                "idade_atual": cliente.idade,
                "idade_minima": req["idade_minima"],
                "tempo_faltante_2019": self._arredondar(tempo_faltante_2019),
                "tempo_a_cumprir": self._arredondar(tempo_a_cumprir),
                "tempo_ja_cumprido": self._arredondar(tempo_apos_corte)
            }
        
        return ResultadoRegra(
            nome_regra=self.nome(),
            elegivel=elegivel,
            rmi_estimada=rmi_estimada,
            o_que_falta=o_que_falta,
            detalhes=detalhes
        )
