from sqlalchemy import Column, String, Date, Float, TIMESTAMP, UUID, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.models.base import Base

class SalarioContribuicaoDB(Base):
    __tablename__ = 'salarios_contribuicao'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True)
    
    competencia = Column(Date, nullable=False, index=True)  # Mês/ano da contribuição
    valor = Column(Float, nullable=False)
    origem = Column(String(50), default="manual")  # manual, cnis, holerite
    
    criado_em = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relacionamentos
    cliente = relationship("ClienteDB", back_populates="salarios")
    
    def __repr__(self):
        return f"<Salario {self.competencia} - R${self.valor}>"
    
    class Config:
        indexes = [
            Index('idx_cliente_competencia', 'cliente_id', 'competencia', unique=True)
        ]

from sqlalchemy import Index
