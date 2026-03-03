"""
Teste de formatação - verifica se todos os números têm 2 casas decimais
"""

import sys
import os
from datetime import date
import re

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.models.cliente import Cliente
from app.core.rules.pontos import RegraPontos
from app.core.rules.idade import RegraIdade
from app.core.rules.pedagio_50 import RegraPedagio50

def verificar_formatacao(valor, nome_campo):
    """Verifica se o valor tem no máximo 2 casas decimais quando convertido para string"""
    if isinstance(valor, float):
        str_valor = f"{valor:.10f}"  # força muitas casas decimais
        partes = str_valor.split('.')
        if len(partes) > 1 and len(partes[1]) > 2:
            decimais = len(partes[1].rstrip('0'))
            if decimais > 2:
                print(f"  ⚠️  {nome_campo} tem {decimais} casas decimais: {valor}")
                return False
    return True

def testar_cliente(nome, cliente):
    """Testa um cliente e verifica a formatação"""
    print(f"\n▶ Testando: {nome}")
    print(f"  Idade: {cliente.idade} anos")
    print(f"  Tempo: {cliente.tempo_contribuicao_dias/365.25:.2f} anos")
    
    regras = [RegraPontos(), RegraIdade(), RegraPedagio50()]
    
    for regra in regras:
        resultado = regra.verificar(cliente)
        print(f"\n  {resultado.nome_regra}:")
        print(f"    Elegível: {resultado.elegivel}")
        
        # Verificar formatação do o_que_falta
        if resultado.o_que_falta:
            # Extrair números com regex
            numeros = re.findall(r'\d+\.\d+', resultado.o_que_falta)
            for num in numeros:
                partes = num.split('.')
                if len(partes[1]) > 2:
                    print(f"    ⚠️  Número com muitas casas: {num}")
        
        # Verificar detalhes
        if resultado.detalhes:
            for chave, valor in resultado.detalhes.items():
                if isinstance(valor, float):
                    verificar_formatacao(valor, chave)
        
        if resultado.rmi_estimada:
            verificar_formatacao(resultado.rmi_estimada, "RMI")

# Criar vários clientes para teste
clientes = [
    (
        "Cliente 1 - Homem 60/35",
        Cliente(
            id=None, nome_completo="Teste 1", cpf="111.111.111-11",
            data_nascimento=date(1966, 1, 1), sexo="M",
            categoria_segurado="CLT", data_filiacao_rgps=date(1991, 1, 1),
            tempo_contribuicao_dias=int(35 * 365.25),
            salarios_contribuicao=[3000.0] * 480,
            tem_atividade_especial=False, professor=False,
            atividade_rural=False, deficiencia="nenhuma", vinculos=[]
        )
    ),
    (
        "Cliente 2 - Mulher 55/30", 
        Cliente(
            id=None, nome_completo="Teste 2", cpf="222.222.222-22",
            data_nascimento=date(1971, 1, 1), sexo="F",
            categoria_segurado="CLT", data_filiacao_rgps=date(1996, 1, 1),
            tempo_contribuicao_dias=int(30 * 365.25),
            salarios_contribuicao=[3000.0] * 360,
            tem_atividade_especial=False, professor=False,
            atividade_rural=False, deficiencia="nenhuma", vinculos=[]
        )
    ),
    (
        "Cliente 3 - Não Elegível",
        Cliente(
            id=None, nome_completo="Teste 3", cpf="333.333.333-33",
            data_nascimento=date(1995, 1, 1), sexo="M",
            categoria_segurado="CLT", data_filiacao_rgps=date(2015, 1, 1),
            tempo_contribuicao_dias=int(11 * 365.25),
            salarios_contribuicao=[2500.0] * 132,
            tem_atividade_especial=False, professor=False,
            atividade_rural=False, deficiencia="nenhuma", vinculos=[]
        )
    )
]

print("="*60)
print("🧪 TESTE DE FORMATAÇÃO - 2 CASAS DECIMAIS")
print("="*60)

for nome, cliente in clientes:
    testar_cliente(nome, cliente)

print("\n" + "="*60)
print("✅ TESTE CONCLUÍDO")
print("="*60)
