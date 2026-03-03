from sqlalchemy import Column, String, Date, Boolean, TIMESTAMP, UUID, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from datetime import date

from app.models.base import Base

class TipoVinculoEnum(str, enum.Enum):
    CLT = "CLT"
    AUTONOMO = "autonomo"
    DOMESTICO = "domestico"
    SERVIDOR = "servidor"
    RURAL = "rural"
    MEI = "mei"

class RegimeEnum(str, enum.Enum):
    RGPS = "RGPS"
    RPPS = "RPPS"

class OrigemEnum(str, enum.Enum):
    MANUAL = "manual"
    CNIS = "cnis"

class VinculoDB(Base):
    __tablename__ = 'vinculos'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True)
    
    empregador = Column(String(200), nullable=False, index=True)
    cnpj_cpf_empregador = Column(String(18), nullable=True, index=True)
    
    data_inicio = Column(Date, nullable=False, index=True)
    data_fim = Column(Date, nullable=True)
    
    tipo_vinculo = Column(Enum(TipoVinculoEnum), nullable=False)
    regime = Column(Enum(RegimeEnum), default=RegimeEnum.RGPS)
    origem = Column(Enum(OrigemEnum), default=OrigemEnum.MANUAL)
    divergencia_cnis = Column(Boolean, default=False)
    
    cargo = Column(String(200), nullable=True)
    salario_ultimo = Column(String(20), nullable=True)
    
    criado_em = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relacionamentos
    cliente = relationship("ClienteDB", back_populates="vinculos")
    
    def __repr__(self):
        return f"<Vinculo {self.empregador} - {self.data_inicio}>"
    
    @property
    def duracao_dias(self) -> int:
        fim = self.data_fim if self.data_fim else date.today()
        return (fim - self.data_inicio).days
