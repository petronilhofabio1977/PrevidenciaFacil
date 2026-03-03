#!/bin/bash
echo "🔒 IMPLEMENTANDO SEGURANÇA MÁXIMA"
echo "=================================="

# 1. Backup
echo "📦 Configurando backup..."
./backup_previdencia.sh

# 2. Rate limiting
echo "🚦 Configurando rate limiting..."
cd /home/techmaster/PrevidenciaFacil/backend
source venv/bin/activate
pip install slowapi

# 3. Monitoramento
echo "📊 Configurando monitoramento..."
cd /home/techmaster/PrevidenciaFacil
docker-compose up -d prometheus grafana redis

# 4. Postgres exporter
echo "📈 Configurando exporter do PostgreSQL..."
docker run -d \
  --name postgres_exporter \
  --network previdenciafacil_previdencia_network \
  -e DATA_SOURCE_NAME="postgresql://postgres:postgres@postgres:5432/previdenciadb?sslmode=disable" \
  -p 9187:9187 \
  wrouesnel/postgres_exporter

echo ""
echo "✅ SEGURANÇA IMPLEMENTADA!"
echo "📊 Grafana: http://localhost:3005 (admin/admin123)"
echo "📈 Prometheus: http://localhost:9090"
