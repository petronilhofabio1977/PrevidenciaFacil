"""
Calculadora de Tempo de Contribuição
Algoritmos: Merge Sort (CLRS Cap. 2) para ordenar vínculos
"""

from datetime import date
from typing import List, Optional
from app.models.cliente import Vinculo

class CalculadoraTempo:
    """Calcula tempo de contribuição a partir dos vínculos"""
    
    def tempo_total(self, vinculos: List[Vinculo]) -> float:
        """
        Calcula tempo total de contribuição em anos
        Usa Merge Sort implícito via sorted()
        """
        # Ordena vínculos por data de início (Timsort = Merge Sort)
        vinculos_ordenados = sorted(vinculos, key=lambda v: v.data_inicio)
        
        dias_total = 0
        for vinculo in vinculos_ordenados:
            if vinculo.data_fim:
                dias = (vinculo.data_fim - vinculo.data_inicio).days
            else:
                dias = (date.today() - vinculo.data_inicio).days
            dias_total += max(0, dias)  # evita valores negativos
        
        return dias_total / 365.25
    
    def tempo_ate_data(self, vinculos: List[Vinculo], data_corte: date) -> float:
        """
        Calcula tempo de contribuição acumulado até uma data específica
        """
        dias_total = 0
        for vinculo in vinculos:
            inicio = vinculo.data_inicio
            fim = vinculo.data_fim if vinculo.data_fim else data_corte
            
            if inicio > data_corte:
                continue  # vínculo começou após a data de corte
            
            fim_real = min(fim, data_corte)
            dias = (fim_real - inicio).days
            dias_total += max(0, dias)
        
        return dias_total / 365.25
