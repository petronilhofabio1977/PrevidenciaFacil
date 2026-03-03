from sqlalchemy import Column, String, Boolean, TIMESTAMP, UUID, JSON, Integer, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.models.base import Base

class PlanoEnum(str, enum.Enum):
    GRATUITO = "gratuito"
    BASICO = "basico"
    PROFISSIONAL = "profissional"
    EMPRESARIAL = "empresarial"

class EscritorioDB(Base):
    __tablename__ = 'escritorios'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(200), nullable=False, index=True)
    cnpj = Column(String(18), unique=True, nullable=True, index=True)
    plano = Column(String(50), default=PlanoEnum.GRATUITO.value, index=True)
    data_criacao = Column(TIMESTAMP(timezone=True), server_default=func.now())
    ativo = Column(Boolean, default=True, index=True)
    
    # Configurações
    configuracoes = Column(JSON, nullable=True)
    
    # Limites do plano
    limite_usuarios = Column(Integer, default=1, nullable=False)
    limite_clientes = Column(Integer, default=10, nullable=False)
    limite_documentos = Column(Integer, default=100, nullable=False)
    limite_analises = Column(Integer, default=50, nullable=False)
    
    # Relacionamentos
    usuarios = relationship("UsuarioDB", back_populates="escritorio", cascade="all, delete-orphan")
    clientes = relationship("ClienteDB", back_populates="escritorio", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Escritorio {self.nome}>"
