"""
Teste específico para a regra de Pedágio 50%
"""

import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.cliente import Cliente
from app.core.rules.pedagio_50 import RegraPedagio50

def test_pedagio_50_com_dados_reais():
    """Teste com dados que simulam um caso real de pedágio 50%"""
    
    # Cliente que em 2019 tinha 34 anos de contribuição (faltava 1 ano)
    # e hoje já cumpriu o pedágio
    cliente = Cliente(
        id=None,
        nome_completo="Teste Pedágio Real",
        cpf="123.456.789-02",
        data_nascimento=date(1960, 1, 1),
        sexo="M",
        categoria_segurado="CLT",
        data_filiacao_rgps=date(1985, 1, 1),  # 34 anos até 2019
        tempo_contribuicao_dias=int(37 * 365.25),  # 37 anos hoje
        salarios_contribuicao=[4000.0] * 444,  # 37 anos de salários
        tem_atividade_especial=False,
        professor=False,
        atividade_rural=False,
        deficiencia="nenhuma",
        vinculos=[]
    )
    
    regra = RegraPedagio50()
    resultado = regra.verificar(cliente)
    
    print(f"\n{'='*60}")
    print(f"TESTE PEDÁGIO 50%")
    print(f"{'='*60}")
    print(f"Cliente: {cliente.nome_completo}")
    print(f"Data filiação: {cliente.data_filiacao_rgps}")
    print(f"Tempo contribuição: {cliente.tempo_contribuicao_dias/365.25:.1f} anos")
    print(f"{'-'*60}")
    print(f"Regra: {resultado.nome_regra}")
    print(f"Elegível: {'✅ SIM' if resultado.elegivel else '❌ NÃO'}")
    print(f"Mensagem: {resultado.o_que_falta}")
    if resultado.rmi_estimada:
        print(f"RMI Estimada: R$ {resultado.rmi_estimada:.2f}")
    print(f"Detalhes: {resultado.detalhes}")
    print(f"{'='*60}")
    
    assert resultado.elegivel == True, "Cliente deveria ser elegível para pedágio 50%"

if __name__ == "__main__":
    test_pedagio_50_com_dados_reais()
