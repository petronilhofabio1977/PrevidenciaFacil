#!/usr/bin/env python
"""
Script para testar o MotorPrevidenciario com diferentes perfis de clientes
"""

import sys
import os
from datetime import date
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.cliente import Cliente
from app.core.engine import MotorPrevidenciario

def criar_cliente_teste(tipo: str) -> Cliente:
    """Cria diferentes perfis de clientes para teste"""
    
    clientes = {
        "professor": Cliente(
            id=None,
            nome_completo="Professor Carlos",
            cpf="111.222.333-44",
            data_nascimento=date(1966, 1, 1),
            sexo="M",
            categoria_segurado="CLT",
            data_filiacao_rgps=date(1991, 1, 1),
            professor=True,
            atividade_rural=False,
            deficiencia="nenhuma",
            tempo_contribuicao_dias=int(35 * 365.25),
            salarios_contribuicao=[5000.0] * 420,
            tem_atividade_especial=False,
            vinculos=[],
            periodos_especiais=[]
        ),
        
        "rural": Cliente(
            id=None,
            nome_completo="Maria Rural",
            cpf="222.333.444-55",
            data_nascimento=date(1971, 1, 1),
            sexo="F",
            categoria_segurado="RURAL",
            data_filiacao_rgps=date(1996, 1, 1),
            professor=False,
            atividade_rural=True,
            deficiencia="nenhuma",
            tempo_contribuicao_dias=int(30 * 365.25),
            salarios_contribuicao=[3000.0] * 360,
            tem_atividade_especial=False,
            vinculos=[],
            periodos_especiais=[]
        ),
        
        "especial": Cliente(
            id=None,
            nome_completo="João Especial",
            cpf="333.444.555-66",
            data_nascimento=date(1970, 1, 1),
            sexo="M",
            categoria_segurado="CLT",
            data_filiacao_rgps=date(1990, 1, 1),
            professor=False,
            atividade_rural=False,
            deficiencia="nenhuma",
            tempo_contribuicao_dias=int(36 * 365.25),
            salarios_contribuicao=[4500.0] * 432,
            tem_atividade_especial=True,
            vinculos=[],
            periodos_especiais=[]
        ),
        
        "deficiente": Cliente(
            id=None,
            nome_completo="Ana Deficiente",
            cpf="444.555.666-77",
            data_nascimento=date(1975, 1, 1),
            sexo="F",
            categoria_segurado="CLT",
            data_filiacao_rgps=date(1995, 1, 1),
            professor=False,
            atividade_rural=False,
            deficiencia="leve",
            tempo_contribuicao_dias=int(25 * 365.25),
            salarios_contribuicao=[4000.0] * 300,
            tem_atividade_especial=False,
            vinculos=[],
            periodos_especiais=[]
        ),
        
        "jovem": Cliente(
            id=None,
            nome_completo="Pedro Jovem",
            cpf="555.666.777-88",
            data_nascimento=date(1995, 1, 1),
            sexo="M",
            categoria_segurado="CLT",
            data_filiacao_rgps=date(2015, 1, 1),
            professor=False,
            atividade_rural=False,
            deficiencia="nenhuma",
            tempo_contribuicao_dias=int(11 * 365.25),
            salarios_contribuicao=[3500.0] * 132,
            tem_atividade_especial=False,
            vinculos=[],
            periodos_especiais=[]
        )
    }
    
    return clientes.get(tipo, clientes["jovem"])

def testar_cliente(cliente: Cliente, nome_teste: str):
    """Executa teste completo para um cliente"""
    
    print("\n" + "="*80)
    print(f"🧪 TESTE: {nome_teste}")
    print("="*80)
    print(f"Cliente: {cliente.nome_completo}")
    print(f"Idade: {cliente.idade} anos")
    print(f"Tempo: {cliente.tempo_contribuicao_anos:.1f} anos")
    print(f"Professor: {cliente.professor}")
    print(f"Rural: {cliente.atividade_rural}")
    print(f"Deficiência: {cliente.deficiencia}")
    print(f"Especial: {cliente.tem_atividade_especial}")
    print("-"*80)
    
    motor = MotorPrevidenciario()
    
    print("\n📊 ANALISANDO...\n")
    resultados = motor.analisar(cliente)
    recomendacao = motor.recomendar(cliente)
    
    for i, r in enumerate(resultados, 1):
        status = "✅ ELEGÍVEL" if r.elegivel else "❌ NÃO ELEGÍVEL"
        print(f"{i}. {r.nome_regra}")
        print(f"   Status: {status}")
        if r.elegivel and r.rmi_estimada:
            print(f"   RMI: R$ {r.rmi_estimada:.2f}")
        if r.o_que_falta:
            print(f"   → {r.o_que_falta}")
        print()
    
    print("🎯 RECOMENDAÇÃO FINAL")
    print("-"*40)
    if recomendacao["recomendacao"]:
        print(f"✅ Melhor opção: {recomendacao['recomendacao']}")
        print(f"💰 {recomendacao['motivo_recomendacao']}")
    else:
        print(f"❌ {recomendacao['motivo_recomendacao']}")
        if recomendacao.get("proximo_beneficio"):
            prox = recomendacao["proximo_beneficio"]
            print(f"⏳ Mais próximo: {prox['nome_regra']} (faltam {prox['meses_faltando']} meses)")
    
    print("="*80)

if __name__ == "__main__":
    print("🚀 INICIANDO TESTES DO MOTOR PREVIDENCIÁRIO")
    print("="*80)
    
    perfis = [
        ("professor", "Professor Homem - 60 anos"),
        ("rural", "Mulher Rural - 55 anos"),
        ("especial", "Homem com Atividade Especial"),
        ("deficiente", "Mulher com Deficiência Leve"),
        ("jovem", "Cliente Jovem (não elegível)")
    ]
    
    for tipo, nome in perfis:
        cliente = criar_cliente_teste(tipo)
        testar_cliente(cliente, nome)
        input("\nPressione Enter para continuar...")
    
    print("\n✅ TODOS OS TESTES CONCLUÍDOS!")
