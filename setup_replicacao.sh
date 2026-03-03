#!/bin/bash
echo "🔄 Configurando replicação PostgreSQL..."

# No mestre (postgres principal)
docker exec previdencia_postgres psql -U postgres -c "
CREATE USER replicador WITH REPLICATION ENCRYPTED PASSWORD 'replicador123';
ALTER SYSTEM SET wal_level = replica;
ALTER SYSTEM SET max_wal_senders = 3;
ALTER SYSTEM SET wal_keep_size = '1GB';
"

# Reiniciar mestre
docker-compose restart postgres

echo "✅ Replicação configurada (execute o próximo comando após reiniciar)"
