"""
Regra de Pontos (Transição)
Base legal: Art. 15 da EC 103/2019
"""

from datetime import date
import json
import os
from app.core.rules import RegraBase, ResultadoRegra
from app.models.cliente import Cliente

class RegraPontos(RegraBase):
    """
    Regra de Aposentadoria por Pontos (Transição)
    """
    
    def __init__(self):
        self.tabela_pontos = self._carregar_tabela()
    
    def _carregar_tabela(self):
        """Carrega a tabela de progressão de pontos do arquivo JSON"""
        try:
            caminho = os.path.join(
                os.path.dirname(__file__), 
                '..', 'tables', 'pontos.json'
            )
            with open(caminho, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "2026": {"homem": 93, "mulher": 83},
                "2027": {"homem": 94, "mulher": 84},
                "2028": {"homem": 105, "mulher": 100}
            }
    
    def nome(self) -> str:
        return "Regra de Pontos (Transição)"
    
    def _arredondar(self, valor: float, casas: int = 2) -> float:
        """Arredonda valor para o número especificado de casas decimais"""
        return round(valor, casas)
    
    def verificar(self, cliente: Cliente) -> ResultadoRegra:
        """
        Verifica elegibilidade para Regra de Pontos
        """
        # 1. Verificar se tem direito à transição
        if not cliente.elegivel_transicao:
            return ResultadoRegra(
                nome_regra=self.nome(),
                elegivel=False,
                o_que_falta="Cliente não tem direito às regras de transição (filiado após 13/11/2019)",
                detalhes={"motivo": "pos_reforma"}
            )
        
        # 2. Verificar tempo mínimo de contribuição (com margem de erro)
        tempo_contribuicao_anos = self._arredondar(cliente.tempo_contribuicao_dias / 365.25)
        
        if cliente.sexo == "M":
            if tempo_contribuicao_anos < 34.9:
                return ResultadoRegra(
                    nome_regra=self.nome(),
                    elegivel=False,
                    o_que_falta=f"Tempo de contribuição insuficiente: {tempo_contribuicao_anos:.2f}/35 anos",
                    detalhes={
                        "tempo_atual": tempo_contribuicao_anos,
                        "tempo_necessario": 35
                    }
                )
        else:  # Feminino
            if tempo_contribuicao_anos < 29.9:
                return ResultadoRegra(
                    nome_regra=self.nome(),
                    elegivel=False,
                    o_que_falta=f"Tempo de contribuição insuficiente: {tempo_contribuicao_anos:.2f}/30 anos",
                    detalhes={
                        "tempo_atual": tempo_contribuicao_anos,
                        "tempo_necessario": 30
                    }
                )
        
        # 3. Calcular pontos
        idade = self._arredondar(cliente.idade_exata if hasattr(cliente, 'idade_exata') else cliente.idade)
        pontos = self._arredondar(idade + tempo_contribuicao_anos)
        
        # 4. Obter pontos mínimos
        ano_atual = date.today().year
        ano_str = str(ano_atual)
        
        if ano_str in self.tabela_pontos:
            if cliente.sexo == "M":
                pontos_minimos = self.tabela_pontos[ano_str]["homem"]
            else:
                pontos_minimos = self.tabela_pontos[ano_str]["mulher"]
        else:
            pontos_minimos = 105 if cliente.sexo == "M" else 100
        
        # 5. Verificar elegibilidade
        elegivel = pontos >= pontos_minimos - 0.01
        
        if elegivel:
            rmi_estimada = None
            if cliente.salarios_contribuicao:
                salarios_ordenados = sorted(cliente.salarios_contribuicao, reverse=True)
                n = len(salarios_ordenados)
                k = int(n * 0.8)
                maiores_80 = salarios_ordenados[:k]
                rmi_estimada = self._arredondar(sum(maiores_80) / len(maiores_80) if maiores_80 else 0)
            
            o_que_falta = None
        else:
            rmi_estimada = None
            pontos_faltando = self._arredondar(pontos_minimos - pontos)
            o_que_falta = f"Faltam {pontos_faltando:.2f} pontos (atual: {pontos:.2f}, necessário: {pontos_minimos})"
        
        detalhes = {
            "idade_atual": idade,
            "tempo_contribuicao_anos": tempo_contribuicao_anos,
            "pontos_atuais": pontos,
            "pontos_necessarios": pontos_minimos,
            "ano_referencia": ano_atual
        }
        
        return ResultadoRegra(
            nome_regra=self.nome(),
            elegivel=elegivel,
            rmi_estimada=rmi_estimada,
            o_que_falta=o_que_falta,
            detalhes=detalhes
        )
