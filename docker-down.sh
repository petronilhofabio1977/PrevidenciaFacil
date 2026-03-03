#!/bin/bash

echo "🛑 Parando containers..."
docker-compose down

echo "🗑️  Removendo volumes (opcional - comentado)"
# docker-compose down -v  # Descomente para remover dados do banco

echo "✅ Finalizado!"
