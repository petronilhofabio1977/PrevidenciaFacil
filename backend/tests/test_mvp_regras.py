"""
Testes unitários para as 3 regras principais do MVP
Conforme documentação da advogada
"""

import pytest
import sys
import os
from datetime import date

# Adiciona o path manualmente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.cliente import Cliente
from app.core.rules.pontos import RegraPontos
from app.core.rules.pedagio_50 import RegraPedagio50
from app.core.rules.idade import RegraIdade

def test_regra_pontos_homem_2026():
    """Teste: Homem com 60 anos e 35 anos de contribuição em 2026"""
    cliente = Cliente(
        id=None,
        nome_completo="Teste Homem Pontos",
        cpf="123.456.789-00",
        data_nascimento=date(1966, 1, 1),  # 60 anos em 2026
        sexo="M",
        categoria_segurado="CLT",
        data_filiacao_rgps=date(1991, 1, 1),  # Antes da reforma
        tempo_contribuicao_dias=int(35 * 365.25),
        salarios_contribuicao=[3000.0] * 480,
        tem_atividade_especial=False,
        professor=False,
        atividade_rural=False,
        deficiencia="nenhuma",
        vinculos=[]
    )
    
    regra = RegraPontos()
    resultado = regra.verificar(cliente)
    
    # Em 2026: 60 + 35 = 95 pontos - precisa 93
    assert resultado.elegivel == True
    assert resultado.rmi_estimada is not None
    assert resultado.rmi_estimada > 0
    print(f"\n✓ Regra Pontos (H): {resultado.nome_regra} - Elegível: {resultado.elegivel}")
    print(f"  RMI Estimada: R$ {resultado.rmi_estimada:.2f}")

def test_regra_pontos_mulher_2026():
    """Teste: Mulher com 55 anos e 30 anos de contribuição em 2026"""
    cliente = Cliente(
        id=None,
        nome_completo="Teste Mulher Pontos",
        cpf="123.456.789-01",
        data_nascimento=date(1971, 1, 1),  # 55 anos em 2026
        sexo="F",
        categoria_segurado="CLT",
        data_filiacao_rgps=date(1996, 1, 1),  # Antes da reforma
        tempo_contribuicao_dias=int(30 * 365.25),
        salarios_contribuicao=[3000.0] * 360,
        tem_atividade_especial=False,
        professor=False,
        atividade_rural=False,
        deficiencia="nenhuma",
        vinculos=[]
    )
    
    regra = RegraPontos()
    resultado = regra.verificar(cliente)
    
    # Em 2026: 55 + 30 = 85 pontos - precisa 83
    assert resultado.elegivel == True
    assert resultado.rmi_estimada is not None
    assert resultado.rmi_estimada > 0
    print(f"\n✓ Regra Pontos (M): {resultado.nome_regra} - Elegível: {resultado.elegivel}")
    print(f"  RMI Estimada: R$ {resultado.rmi_estimada:.2f}")

def test_regra_pedagio50_elegivel():
    """Teste: Quem faltava 1 ano em 2019"""
    cliente = Cliente(
        id=None,
        nome_completo="Teste Pedágio 50%",
        cpf="123.456.789-02",
        data_nascimento=date(1960, 1, 1),
        sexo="M",
        categoria_segurado="CLT",
        data_filiacao_rgps=date(1985, 1, 1),  # Antes da reforma
        tempo_contribuicao_dias=int(36 * 365.25),  # Já cumpriu o pedágio
        salarios_contribuicao=[4000.0] * 480,
        tem_atividade_especial=False,
        professor=False,
        atividade_rural=False,
        deficiencia="nenhuma",
        vinculos=[]
    )
    
    regra = RegraPedagio50()
    resultado = regra.verificar(cliente)
    
    # Deve ser elegível
    assert resultado.elegivel == True
    print(f"\n✓ Regra Pedágio 50%: {resultado.nome_regra} - Elegível: {resultado.elegivel}")
    if resultado.rmi_estimada:
        print(f"  RMI Estimada: R$ {resultado.rmi_estimada:.2f}")

def test_regra_idade_homem():
    """Teste: Homem com 65 anos e 20 anos de contribuição"""
    cliente = Cliente(
        id=None,
        nome_completo="Teste Idade Homem",
        cpf="123.456.789-03",
        data_nascimento=date(1961, 1, 1),  # 65 anos em 2026
        sexo="M",
        categoria_segurado="CLT",
        data_filiacao_rgps=date(2006, 1, 1),  # 20 anos
        tempo_contribuicao_dias=int(20 * 365.25),
        salarios_contribuicao=[3500.0] * 240,
        tem_atividade_especial=False,
        professor=False,
        atividade_rural=False,
        deficiencia="nenhuma",
        vinculos=[]
    )
    
    regra = RegraIdade()
    resultado = regra.verificar(cliente)
    
    assert resultado.elegivel == True
    assert resultado.rmi_estimada is not None
    assert resultado.rmi_estimada > 0
    print(f"\n✓ Regra Idade (H): {resultado.nome_regra} - Elegível: {resultado.elegivel}")
    print(f"  RMI Estimada: R$ {resultado.rmi_estimada:.2f}")

def test_regra_idade_mulher():
    """Teste: Mulher com 62 anos e 15 anos de contribuição"""
    cliente = Cliente(
        id=None,
        nome_completo="Teste Idade Mulher",
        cpf="123.456.789-04",
        data_nascimento=date(1964, 1, 1),  # 62 anos em 2026
        sexo="F",
        categoria_segurado="CLT",
        data_filiacao_rgps=date(2011, 1, 1),  # 15 anos
        tempo_contribuicao_dias=int(15 * 365.25),
        salarios_contribuicao=[3500.0] * 180,
        tem_atividade_especial=False,
        professor=False,
        atividade_rural=False,
        deficiencia="nenhuma",
        vinculos=[]
    )
    
    regra = RegraIdade()
    resultado = regra.verificar(cliente)
    
    assert resultado.elegivel == True
    assert resultado.rmi_estimada is not None
    assert resultado.rmi_estimada > 0
    print(f"\n✓ Regra Idade (M): {resultado.nome_regra} - Elegível: {resultado.elegivel}")
    print(f"  RMI Estimada: R$ {resultado.rmi_estimada:.2f}")

def test_nao_elegivel():
    """Teste: Cliente não elegível"""
    cliente = Cliente(
        id=None,
        nome_completo="Teste Não Elegível",
        cpf="123.456.789-05",
        data_nascimento=date(1990, 1, 1),  # 36 anos
        sexo="M",
        categoria_segurado="CLT",
        data_filiacao_rgps=date(2010, 1, 1),  # 16 anos
        tempo_contribuicao_dias=int(10 * 365.25),
        salarios_contribuicao=[2500.0] * 120,
        tem_atividade_especial=False,
        professor=False,
        atividade_rural=False,
        deficiencia="nenhuma",
        vinculos=[]
    )
    
    regra_pontos = RegraPontos()
    resultado_pontos = regra_pontos.verificar(cliente)
    
    regra_idade = RegraIdade()
    resultado_idade = regra_idade.verificar(cliente)
    
    assert resultado_pontos.elegivel == False
    assert resultado_idade.elegivel == False
    assert resultado_pontos.o_que_falta is not None
    assert resultado_idade.o_que_falta is not None
    print(f"\n✗ Teste Não Elegível:")
    print(f"  Pontos: {resultado_pontos.o_que_falta}")
    print(f"  Idade: {resultado_idade.o_que_falta}")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
