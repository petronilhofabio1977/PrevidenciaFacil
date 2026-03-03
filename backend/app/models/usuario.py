from sqlalchemy import Column, String, Boolean, TIMESTAMP, UUID, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime

from app.models.base import Base

class UsuarioDB(Base):
    __tablename__ = 'usuarios'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    escritorio_id = Column(UUID(as_uuid=True), ForeignKey('escritorios.id', ondelete='CASCADE'), nullable=False, index=True)
    
    nome = Column(String(200), nullable=False, index=True)
    email = Column(String(200), unique=True, nullable=False, index=True)
    senha_hash = Column(String(200), nullable=False)
    
    # Perfil profissional
    oab = Column(String(20), nullable=True, index=True)
    telefone = Column(String(20), nullable=True)
    avatar = Column(String(500), nullable=True)
    
    # Permissões
    is_admin = Column(Boolean, default=False, index=True)
    permissoes = Column(JSON, nullable=True)  # {"clientes": "crud", "documentos": "r", ...}
    
    # Controle
    ultimo_acesso = Column(TIMESTAMP(timezone=True), nullable=True)
    criado_em = Column(TIMESTAMP(timezone=True), server_default=func.now(), index=True)
    ativo = Column(Boolean, default=True, index=True)
    
    # Relacionamentos
    escritorio = relationship("EscritorioDB", back_populates="usuarios")
    clientes_criados = relationship("ClienteDB", back_populates="usuario", foreign_keys="[ClienteDB.usuario_id]")
    
    def __repr__(self):
        return f"<Usuario {self.email}>"
