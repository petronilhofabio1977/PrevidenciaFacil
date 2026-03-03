#!/bin/bash
# Script de backup automático do PrevidênciaFácil

BACKUP_DIR="/backup/previdenciadb"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Criar diretório se não existir
mkdir -p $BACKUP_DIR

echo "📦 Iniciando backup em $DATE"

# Backup do banco de dados
docker exec previdencia_postgres pg_dump -U postgres -d previdenciadb | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup dos uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /home/techmaster/PrevidenciaFacil/backend/uploads

# Remover backups antigos (mais de 30 dias)
find $BACKUP_DIR -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "✅ Backup concluído em $BACKUP_DIR/db_$DATE.sql.gz"
