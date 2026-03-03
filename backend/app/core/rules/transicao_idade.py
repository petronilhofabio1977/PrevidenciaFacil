"""
Regra de Transição por Idade (Idade Progressiva)
Base legal: Art. 16 da EC 103/2019
- Tempo de contribuição: 35 anos (H) / 30 anos (M)
- Idade em 2026: 64,5 anos (H) / 59,5 anos (M)
- Sobe 6 meses por ano até 65/62 em 2031
"""

from datetime import date
from app.core.rules import RegraBase, ResultadoRegra
from app.models.cliente import Cliente

class RegraTransicaoIdade(RegraBase):
    """
    Regra de Transição por Idade (Idade Progressiva)
    """
    
    def __init__(self):
        self.data_corte = date(2019, 11, 13)
        self.ano_base = 2020
        self.idade_inicial = {
            "M": 61.5,  # 61 anos e 6 meses em 2020
            "F": 56.5   # 56 anos e 6 meses em 2020
        }
        self.idade_final = {
            "M": 65,    # Em 2031
            "F": 62     # Em 2031
        }
        self.tempo_necessario = {
            "M": 35,
            "F": 30
        }
    
    def nome(self) -> str:
        return "Transição por Idade (Idade Progressiva)"
    
    def _arredondar(self, valor: float, casas: int = 2) -> float:
        return round(valor, casas)
    
    def _idade_minima_ano(self, ano: int, sexo: str) -> float:
        """Calcula idade mínima para um determinado ano"""
        if ano <= 2019:
            return self.idade_inicial[sexo] - 0.5  # Ajuste para 2019
        
        anos_passados = min(ano - self.ano_base, 11)  # Máximo até 2031
        incremento = anos_passados * 0.5  # 6 meses por ano
        
        idade = self.idade_inicial[sexo] + incremento
        return min(idade, self.idade_final[sexo])
    
    def verificar(self, cliente: Cliente) -> ResultadoRegra:
        """
        Verifica elegibilidade para Transição por Idade
        """
        if not cliente.elegivel_transicao:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Cliente não tem direito às regras de transição",
                detalhes={"motivo": "pos_reforma"}
            )
        
        # Verificar tempo de contribuição
        tempo_contribuicao_anos = cliente.tempo_contribuicao_dias / 365.25
        tempo_necessario = self.tempo_necessario.get(cliente.sexo, 0)
        
        if tempo_contribuicao_anos < tempo_necessario - 0.01:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta=f"Tempo de contribuição insuficiente: {self._arredondar(tempo_contribuicao_anos)}/{tempo_necessario} anos",
                detalhes={"tempo_atual": self._arredondar(tempo_contribuicao_anos), "tempo_necessario": tempo_necessario}
            )
        
        # Verificar idade para o ano atual
        ano_atual = date.today().year
        idade_minima = self._idade_minima_ano(ano_atual, cliente.sexo)
        
        idade_ok = cliente.idade_exata >= idade_minima - 0.01
        
        if idade_ok:
            # Calcular RMI (média dos 80% maiores)
            rmi_estimada = None
            if cliente.salarios_contribuicao:
                salarios_ordenados = sorted(cliente.salarios_contribuicao, reverse=True)
                n = len(salarios_ordenados)
                k = int(n * 0.8)
                maiores_80 = salarios_ordenados[:k]
                media = sum(maiores_80) / len(maiores_80) if maiores_80 else 0
                
                # Fator previdenciário (opcional - depende da regra)
                rmi_estimada = self._arredondar(media)
            
            o_que_falta = None
            detalhes = {
                "idade_atual": cliente.idade_exata,
                "idade_minima_ano": self._arredondar(idade_minima),
                "ano_referencia": ano_atual,
                "tempo_contribuicao": self._arredondar(tempo_contribuicao_anos)
            }
        else:
            anos_faltando = idade_minima - cliente.idade_exata
            o_que_falta = f"Faltam {self._arredondar(anos_faltando)} anos de idade para {ano_atual}"
            rmi_estimada = None
            detalhes = {
                "idade_atual": cliente.idade_exata,
                "idade_minima_ano": self._arredondar(idade_minima),
                "ano_referencia": ano_atual
            }
        
        return ResultadoRegra(
            nome_regra=self.nome(),
            elegivel=idade_ok,
            rmi_estimada=rmi_estimada,
            o_que_falta=o_que_falta,
            detalhes=detalhes
        )
