from sqlalchemy import Column, String, Date, Float, TIMESTAMP, UUID, ForeignKey, JSON, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.models.base import Base

class AnaliseDB(Base):
    __tablename__ = 'analises'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id', ondelete='SET NULL'), nullable=True)
    
    data_analise = Column(TIMESTAMP(timezone=True), server_default=func.now(), index=True)
    data_referencia = Column(Date, nullable=False, server_default=func.now())
    
    # Resultado geral
    resultado_geral = Column(JSON, nullable=False)  # {"elegiveis": [...], "recomendacao": "..."}
    
    # Estatísticas
    total_regras_analisadas = Column(Integer, default=10)
    total_regras_elegiveis = Column(Integer, default=0)
    
    # Controle
    observacoes = Column(String(1000), nullable=True)
    
    # Relacionamentos
    cliente = relationship("ClienteDB", back_populates="analises")
    usuario = relationship("UsuarioDB")
    resultados_regras = relationship("ResultadoRegraDB", back_populates="analise", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Analise {self.cliente_id} - {self.data_analise}>"

class ResultadoRegraDB(Base):
    __tablename__ = 'resultados_regras'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analise_id = Column(UUID(as_uuid=True), ForeignKey('analises.id', ondelete='CASCADE'), nullable=False, index=True)
    
    nome_regra = Column(String(100), nullable=False, index=True)
    elegivel = Column(Boolean, default=False, index=True)
    rmi_estimada = Column(Float, nullable=True)
    o_que_falta = Column(String(500), nullable=True)
    detalhes = Column(JSON, nullable=True)
    
    # Relacionamentos
    analise = relationship("AnaliseDB", back_populates="resultados_regras")
    
    def __repr__(self):
        return f"<Resultado {self.nome_regra} - {self.elegivel}>"
