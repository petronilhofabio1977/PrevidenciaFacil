"""
Calculadora do Fator Previdenciário
Fórmula: Lei 9.876/1999
f = (Tc * a / Es) * [1 + (Id + Tc * a) / 100]
"""

class CalculadoraFatorPrevidenciario:
    """Calcula o fator previdenciário conforme fórmula legal"""
    
    ALIQUOTA = 0.31  # 'a' na fórmula - 31%
    
    def calcular(self, idade: float, tempo_contribuicao_anos: float, 
                 expectativa_vida: float) -> float:
        """
        Calcula fator previdenciário
        
        Args:
            idade: Idade do segurado em anos
            tempo_contribuicao_anos: Tempo de contribuição em anos
            expectativa_vida: Expectativa de sobrevida na idade (tabela IBGE)
        
        Returns:
            Fator previdenciário (float)
        """
        Tc = tempo_contribuicao_anos
        a = self.ALIQUOTA
        Es = expectativa_vida
        Id = idade
        
        # f = (Tc * a / Es) * [1 + (Id + Tc * a) / 100]
        f = (Tc * a / Es) * (1 + (Id + Tc * a) / 100)
        
        return max(1.0, f)  # Fator nunca é menor que 1 (Lei 9.876/1999)
