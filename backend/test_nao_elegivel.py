import sys
import os
from datetime import date
from pprint import pprint

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.models.cliente import Cliente
from app.core.rules.pontos import RegraPontos
from app.core.rules.idade import RegraIdade
from app.core.rules.pedagio_50 import RegraPedagio50

# Cliente jovem com pouco tempo de contribuição
cliente = Cliente(
    id=None,
    nome_completo="João Jovem",
    cpf="123.456.789-99",
    data_nascimento=date(1995, 1, 1),  # 31 anos
    sexo="M",
    categoria_segurado="CLT",
    data_filiacao_rgps=date(2015, 1, 1),  # 11 anos
    tempo_contribuicao_dias=int(11 * 365.25),
    salarios_contribuicao=[3000.0] * 132,
    tem_atividade_especial=False,
    professor=False,
    atividade_rural=False,
    deficiencia="nenhuma",
    vinculos=[]
)

print("="*60)
print("TESTE: CLIENTE NÃO ELEGÍVEL")
print("="*60)
print(f"Nome: {cliente.nome_completo}")
print(f"Idade: {cliente.idade} anos")
print(f"Tempo contribuição: {cliente.tempo_contribuicao_dias/365.25:.1f} anos")
print("="*60)

# Testar cada regra
regras = [RegraPontos(), RegraIdade(), RegraPedagio50()]

for regra in regras:
    resultado = regra.verificar(cliente)
    print(f"\n▶ {resultado.nome_regra}")
    print(f"  Elegível: {'✅' if resultado.elegivel else '❌'}")
    if not resultado.elegivel:
        print(f"  ⚠️  O QUE FALTA: {resultado.o_que_falta}")
        print(f"  📊 Detalhes: {resultado.detalhes}")
