from sqlalchemy import Column, String, Date, Boolean, TIMESTAMP, UUID, ForeignKey, Integer, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.models.base import Base

class TipoDocumentoEnum(str, enum.Enum):
    RG = "rg"
    CPF = "cpf"
    CNH = "cnh"
    CERTIDAO_NASCIMENTO = "certidao_nascimento"
    CERTIDAO_CASAMENTO = "certidao_casamento"
    COMPROVANTE_RESIDENCIA = "comprovante_residencia"
    CTPS = "ctps"
    CNIS = "cnis"
    CARNE_GPS = "carne_gps"
    HOLERITE = "holerite"
    FGTS = "fgts"
    IRPF = "irpf"
    PPP = "ppp"
    LTCAT = "ltcat"
    LAUDO_MEDICO = "laudo_medico"
    AUTO_DECLARACAO_RURAL = "auto_declaracao_rural"
    CERTIFICADO_RESERVISTA = "certificado_reservista"
    OUTRO = "outro"

class StatusDocumentoEnum(str, enum.Enum):
    PENDENTE = "pendente"
    VALIDADO = "validado"
    INVALIDO = "invalido"
    EM_ANALISE = "em_analise"

class DocumentoDB(Base):
    __tablename__ = 'documentos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Metadados do arquivo
    nome_arquivo = Column(String(500), nullable=False)
    caminho_arquivo = Column(String(1000), nullable=False)
    tamanho_bytes = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)
    hash_arquivo = Column(String(64), nullable=True, index=True)
    
    # Classificação
    tipo_documento = Column(String(50), nullable=False, index=True)
    subtipo = Column(String(100), nullable=True)
    data_referencia = Column(Date, nullable=True, index=True)
    data_validade = Column(Date, nullable=True)
    
    # Validação
    status = Column(String(50), default=StatusDocumentoEnum.PENDENTE.value, index=True)
    data_validacao = Column(TIMESTAMP(timezone=True), nullable=True)
    validado_por = Column(String(200), nullable=True)
    
    # Resultados
    validacao_resultado = Column(JSON, nullable=True)
    observacoes = Column(String(1000), nullable=True)
    alertas = Column(JSON, nullable=True)
    
    # Controle
    criado_em = Column(TIMESTAMP(timezone=True), server_default=func.now(), index=True)
    atualizado_em = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    cliente = relationship("ClienteDB", back_populates="documentos")
    
    def __repr__(self):
        return f"<Documento {self.nome_arquivo}>"
