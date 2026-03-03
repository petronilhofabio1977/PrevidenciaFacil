#!/usr/bin/env python
"""
Script para testar a análise completa com todas as 10 regras
"""

import sys
import os
from datetime import date
from pprint import pprint

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.models.cliente import Cliente
from app.core.engine import MotorPrevidenciario

def criar_cliente_teste():
    """Cria um cliente de teste com dados completos"""
    
    # Cliente: Homem, 60 anos, 35 anos de contribuição
    # Professor, sem atividade especial, sem deficiência
    cliente = Cliente(
        id=None,
        nome_completo="João da Silva Professor",
        cpf="123.456.789-00",
        data_nascimento=date(1966, 1, 1),  # 60 anos em 2026
        sexo="M",
        categoria_segurado="CLT",
        data_filiacao_rgps=date(1991, 1, 1),  # 35 anos até 2026
        professor=True,  # É professor
        atividade_rural=False,
        deficiencia="nenhuma",
        tempo_contribuicao_dias=int(35 * 365.25),  # 35 anos
        salarios_contribuicao=[3500.0] * 420,  # 35 anos de salários
        tem_atividade_especial=False,
        vinculos=[],
        periodos_especiais=[]
    )
    
    return cliente

def criar_cliente_mulher_teste():
    """Cria uma cliente mulher para teste"""
    
    cliente = Cliente(
        id=None,
        nome_completo="Maria Oliveira",
        cpf="987.654.321-00",
        data_nascimento=date(1971, 1, 1),  # 55 anos em 2026
        sexo="F",
        categoria_segurado="CLT",
        data_filiacao_rgps=date(1996, 1, 1),  # 30 anos até 2026
        professor=False,
        atividade_rural=True,  # Tem atividade rural
        deficiencia="leve",  # Deficiência leve
        tempo_contribuicao_dias=int(30 * 365.25),  # 30 anos
        salarios_contribuicao=[3200.0] * 360,  # 30 anos de salários
        tem_atividade_especial=False,
        vinculos=[],
        periodos_especiais=[]
    )
    
    return cliente

def criar_cliente_especial():
    """Cliente com atividade especial"""
    
    cliente = Cliente(
        id=None,
        nome_completo="Carlos Especial",
        cpf="111.222.333-44",
        data_nascimento=date(1970, 1, 1),  # 56 anos
        sexo="M",
        categoria_segurado="CLT",
        data_filiacao_rgps=date(1990, 1, 1),
        professor=False,
        atividade_rural=False,
        deficiencia="nenhuma",
        tempo_contribuicao_dias=int(36 * 365.25),  # 36 anos
        salarios_contribuicao=[4500.0] * 432,
        tem_atividade_especial=True,  # Tem atividade especial
        vinculos=[],
        periodos_especiais=[]
    )
    
    return cliente

def analisar_cliente(cliente, nome_teste):
    """Executa análise completa para um cliente"""
    
    print("=" * 80)
    print(f"📋 ANÁLISE PREVIDENCIÁRIA COMPLETA - {nome_teste}")
    print("=" * 80)
    print(f"Cliente: {cliente.nome_completo}")
    print(f"CPF: {cliente.cpf}")
    print(f"Data Nascimento: {cliente.data_nascimento}")
    print(f"Sexo: {cliente.sexo}")
    print(f"Idade: {cliente.idade} anos")
    print(f"Idade exata: {cliente.idade_exata} anos")
    print(f"Tempo Contribuição: {cliente.tempo_contribuicao_anos} anos")
    print(f"Professor: {'Sim' if cliente.professor else 'Não'}")
    print(f"Atividade Rural: {'Sim' if cliente.atividade_rural else 'Não'}")
    print(f"Deficiência: {cliente.deficiencia}")
    print(f"Atividade Especial: {'Sim' if cliente.tem_atividade_especial else 'Não'}")
    print(f"Elegível Transição: {'Sim' if cliente.elegivel_transicao else 'Não'}")
    print("-" * 80)
    
    # Inicializar motor com todas as 10 regras
    motor = MotorPrevidenciario()
    
    # Executar análise
    resultados = motor.analisar(cliente)
    recomendacao = motor.mais_vantajoso(resultados)
    
    # Mostrar resultados por regra
    print("\n📊 RESULTADOS POR REGRA:")
    print("-" * 80)
    
    for i, r in enumerate(resultados, 1):
        status = "✅ ELEGÍVEL" if r.elegivel else "❌ NÃO ELEGÍVEL"
        print(f"\n{i}. {r.nome_regra}")
        print(f"   Status: {status}")
        if r.elegivel and r.rmi_estimada:
            print(f"   RMI Estimada: R$ {r.rmi_estimada:.2f}")
        if r.o_que_falta:
            print(f"   {r.o_que_falta}")
        if r.detalhes:
            print(f"   Detalhes: {r.detalhes}")
    
    # Mostrar recomendação final
    print("\n" + "=" * 80)
    print("🎯 RECOMENDAÇÃO FINAL")
    print("=" * 80)
    if recomendacao:
        print(f"✅ Melhor opção: {recomendacao.nome_regra}")
        print(f"💰 RMI Estimada: R$ {recomendacao.rmi_estimada:.2f}")
        print(f"📝 Motivo: {recomendacao.o_que_falta or 'Elegível com maior valor'}")
    else:
        print("❌ Nenhuma regra elegível encontrada")
    
    # Listar regras elegíveis
    elegiveis = [r.nome_regra for r in resultados if r.elegivel]
    if elegiveis:
        print(f"\n📌 Regras elegíveis: {', '.join(elegiveis)}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    print("🚀 INICIANDO ANÁLISE PREVIDENCIÁRIA COMPLETA")
    print("=" * 80)
    
    # Criar clientes de teste
    cliente1 = criar_cliente_teste()
    cliente2 = criar_cliente_mulher_teste()
    cliente3 = criar_cliente_especial()
    
    # Analisar cada cliente
    analisar_cliente(cliente1, "Professor Homem - 60 anos")
    analisar_cliente(cliente2, "Mulher com Atividade Rural e Deficiência Leve")
    analisar_cliente(cliente3, "Homem com Atividade Especial")
    
    print("\n✅ ANÁLISE CONCLUÍDA!")
