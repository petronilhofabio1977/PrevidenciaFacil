from sqlalchemy import Column, String, Date, Boolean, TIMESTAMP, UUID, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.models.base import Base

class PeriodoEspecialDB(Base):
    __tablename__ = 'periodos_especiais'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True)
    
    data_inicio = Column(Date, nullable=False, index=True)
    data_fim = Column(Date, nullable=True)
    
    agente_nocivo = Column(String(200), nullable=False)
    tipo_risco = Column(String(50), nullable=True)  # fisico, quimico, biologico
    intensidade = Column(String(50), default="moderada")  # leve, moderada, grave
    
    ppp_disponivel = Column(Boolean, default=False)
    laudo_tecnico = Column(Boolean, default=False)
    
    criado_em = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relacionamentos
    cliente = relationship("ClienteDB", back_populates="periodos_especiais")
    
    def __repr__(self):
        return f"<PeriodoEspecial {self.data_inicio} - {self.agente_nocivo}>"
    
    @property
    def tempo_especial_anos(self) -> float:
        fim = self.data_fim if self.data_fim else date.today()
        return (fim - self.data_inicio).days / 365.25
