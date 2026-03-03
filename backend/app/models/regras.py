from sqlalchemy import Column, String, Float, Boolean, JSON, TIMESTAMP, UUID, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.models.base import Base

class RegraPrevidenciariaEnum(str, enum.Enum):
    DIREITO_ADQUIRIDO = "Direito Adquirido"
    PONTOS = "Regra de Pontos"
    PEDAGIO_50 = "Pedágio 50%"
    PEDAGIO_100 = "Pedágio 100%"
    IDADE = "Aposentadoria por Idade"
    TRANSICAO_IDADE = "Transição por Idade"
    ESPECIAL = "Aposentadoria Especial"
    PROFESSOR = "Aposentadoria de Professor"
    RURAL = "Aposentadoria Rural"
    DEFICIENTE = "Aposentadoria da Pessoa com Deficiência"

class AnaliseDB(Base):
    __tablename__ = 'analises'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id', ondelete='SET NULL'), nullable=True)
    
    data_analise = Column(TIMESTAMP(timezone=True), server_default=func.now(), index=True)
    data_referencia = Column(Date, nullable=False, server_default=func.now())
    
    # Estatísticas
    total_regras_elegiveis = Column(Integer, default=0)
    melhor_regra = Column(String(100), nullable=True)
    melhor_rmi = Column(Float, nullable=True)
    
    # JSON com resumo
    resumo = Column(JSON, nullable=True)
    
    # Controle
    observacoes = Column(String(1000), nullable=True)
    
    # Relacionamentos
    cliente = relationship("ClienteDB", back_populates="analises")
    usuario = relationship("UsuarioDB")
    resultados = relationship("ResultadoRegraDB", back_populates="analise", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Analise {self.cliente_id} - {self.data_analise}>"

class ResultadoRegraDB(Base):
    __tablename__ = 'resultados_regras'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analise_id = Column(UUID(as_uuid=True), ForeignKey('analises.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Identificação da regra
    regra_id = Column(Integer, nullable=False)
    nome_regra = Column(String(100), nullable=False, index=True)
    
    # Resultado da análise
    elegivel = Column(Boolean, default=False, index=True)
    rmi_estimada = Column(Float, nullable=True)
    o_que_falta = Column(String(500), nullable=True)
    
    # Detalhes específicos da regra
    idade_atual = Column(Integer, nullable=True)
    tempo_contribuicao = Column(Float, nullable=True)
    pontos_atuais = Column(Float, nullable=True)
    pontos_necessarios = Column(Integer, nullable=True)
    tempo_faltante = Column(Float, nullable=True)
    meses_faltando = Column(Integer, nullable=True)
    
    # Campo JSON para detalhes adicionais
    detalhes = Column(JSON, nullable=True)
    
    # Relacionamentos
    analise = relationship("AnaliseDB", back_populates="resultados")
    
    def __repr__(self):
        return f"<Resultado {self.nome_regra} - {self.elegivel}>"

class CacheAnaliseDB(Base):
    __tablename__ = 'cache_analises'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Chave única por cliente + data de referência
    hash_analise = Column(String(64), nullable=False, unique=True, index=True)
    
    data_analise = Column(TIMESTAMP(timezone=True), server_default=func.now())
    data_referencia = Column(Date, nullable=False)
    
    # Resultado em cache
    resultado = Column(JSON, nullable=False)
    
    # Expiração (opcional)
    expira_em = Column(TIMESTAMP(timezone=True), nullable=True)
    
    # Relacionamentos
    cliente = relationship("ClienteDB")
    
    def __repr__(self):
        return f"<Cache {self.cliente_id} - {self.data_referencia}>"
