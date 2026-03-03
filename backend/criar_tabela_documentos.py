from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Text, TIMESTAMP, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

from app.database import engine

print("🚀 Criando tabela de documentos...")

with engine.connect() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id UUID PRIMARY KEY,
            cliente_id UUID NOT NULL,
            nome_arquivo VARCHAR(500) NOT NULL,
            caminho_arquivo VARCHAR(1000) NOT NULL,
            tipo_documento VARCHAR(50) NOT NULL,
            status VARCHAR(50) DEFAULT 'pendente',
            data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tamanho_bytes INTEGER,
            observacoes TEXT
        )
    """)
    conn.commit()

print("✅ Tabela de documentos criada com sucesso!")
