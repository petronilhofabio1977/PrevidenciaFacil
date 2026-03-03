#!/bin/bash

echo "🚀 Iniciando PrevidênciaFácil com Docker"
echo "========================================"

# Parar containers antigos se existirem
docker-compose down

# Construir imagens
echo "📦 Construindo imagens Docker..."
docker-compose build

# Iniciar serviços
echo "🐳 Iniciando containers..."
docker-compose up -d

# Mostrar status
echo "📊 Status dos containers:"
docker-compose ps

echo ""
echo "✅ Sistema iniciado!"
echo "📡 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📚 Documentação: http://localhost:8000/docs"
echo "🗄️ Banco de dados: localhost:5432"
echo ""
echo "📋 Logs: docker-compose logs -f"
