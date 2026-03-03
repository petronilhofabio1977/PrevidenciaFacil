#!/bin/bash
echo "============================================================"
echo "🧪 TESTANDO TODAS AS REGRAS PREVIDENCIÁRIAS"
echo "============================================================"

cd /home/techmaster/PrevidenciaFacil/backend
source venv/bin/activate

echo ""
echo "📋 TESTE 1: Cliente Não Elegível"
echo "------------------------------------------------------------"
python test_nao_elegivel.py

echo ""
echo "📋 TESTE 2: Testes Unitários (pytest)"
echo "------------------------------------------------------------"
python -m pytest tests/test_mvp_regras.py -v

echo ""
echo "📋 TESTE 3: Teste Específico do Pedágio"
echo "------------------------------------------------------------"
python tests/test_pedagio.py

echo ""
echo "📋 TESTE 4: Teste da API (se o servidor estiver rodando)"
echo "------------------------------------------------------------"
curl -s http://localhost:8000/ | python -m json.tool

echo ""
echo "============================================================"
echo "✅ TESTES CONCLUÍDOS"
echo "============================================================"
