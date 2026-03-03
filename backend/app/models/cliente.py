from datetime import date
from sqlalchemy import Column, String, Date, Enum, Boolean, Text, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from datetime import date

from app.models.base import Base

class SexoEnum(str, enum.Enum):
    MASCULINO = "Masculino"
    FEMININO = "Feminino"

class CategoriaSeguradoEnum(str, enum.Enum):
    CLT = "CLT"
    AUTONOMO = "Autônomo"
    MEI = "MEI"
    DOMESTICO = "Doméstico"
    RURAL = "Rural"
    SERVIDOR = "Servidor"

class DeficienciaEnum(str, enum.Enum):
    NENHUMA = "nenhuma"
    LEVE = "leve"
    MODERADA = "moderada"
    GRAVE = "grave"

class ClienteDB(Base):
    __tablename__ = 'clientes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    escritorio_id = Column(UUID(as_uuid=True), ForeignKey('escritorios.id', ondelete='CASCADE'), nullable=False, index=True)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Dados pessoais
    nome_completo = Column(String(200), nullable=False, index=True)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    data_nascimento = Column(Date, nullable=False, index=True)
    sexo = Column(Enum(SexoEnum), nullable=False)
    email = Column(String(200), nullable=True)
    telefone = Column(String(20), nullable=True)
    
    # Categoria
    categoria_segurado = Column(Enum(CategoriaSeguradoEnum), nullable=False)
    data_filiacao_rgps = Column(Date, nullable=True)
    
    # Casos especiais
    professor = Column(Boolean, default=False, index=True)
    atividade_rural = Column(Boolean, default=False, index=True)
    deficiencia = Column(Enum(DeficienciaEnum), default=DeficienciaEnum.NENHUMA, index=True)
    
    # Observações
    observacoes = Column(Text, nullable=True)
    
    # Controle
    criado_em = Column(TIMESTAMP(timezone=True), server_default=func.now(), index=True)
    atualizado_em = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    escritorio = relationship("EscritorioDB", back_populates="clientes")
    usuario = relationship("UsuarioDB", back_populates="clientes_criados", foreign_keys=[usuario_id])
    
    vinculos = relationship("VinculoDB", back_populates="cliente", cascade="all, delete-orphan")
    salarios = relationship("SalarioContribuicaoDB", back_populates="cliente", cascade="all, delete-orphan")
    periodos_especiais = relationship("PeriodoEspecialDB", back_populates="cliente", cascade="all, delete-orphan")
    documentos = relationship("DocumentoDB", back_populates="cliente", cascade="all, delete-orphan")
    analises = relationship("AnaliseDB", back_populates="cliente", cascade="all, delete-orphan")
    analises = relationship("AnaliseDB", back_populates="cliente", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Cliente {self.nome_completo}>"
    
    @property
    def idade(self) -> int:
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

# Classe de domínio (para o motor de regras)
class Cliente:
    """Versão DOMÍNIO (POO pura) para o motor de regras"""
    def __init__(self, id, nome_completo, cpf, data_nascimento, sexo, 
                 categoria_segurado, data_filiacao_rgps=None, professor=False,
                 atividade_rural=False, deficiencia="nenhuma", 
                 tempo_contribuicao_dias=0, salarios_contribuicao=None,
                 tem_atividade_especial=False, vinculos=None, periodos_especiais=None):
        
        self.id = id
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.categoria_segurado = categoria_segurado
        self.data_filiacao_rgps = data_filiacao_rgps
        self.professor = professor
        self.atividade_rural = atividade_rural
        self.deficiencia = deficiencia
        self.tempo_contribuicao_dias = tempo_contribuicao_dias
        self.salarios_contribuicao = salarios_contribuicao or []
        self.tem_atividade_especial = tem_atividade_especial
        self.vinculos = vinculos or []
        self.periodos_especiais = periodos_especiais or []
    
    @property
    def idade(self) -> int:
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
    
    @property
    def idade_exata(self) -> float:
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        
        dia_aniversario = date(hoje.year, self.data_nascimento.month, self.data_nascimento.day)
        if hoje < dia_aniversario:
            dia_aniversario = date(hoje.year - 1, self.data_nascimento.month, self.data_nascimento.day)
        
        dias_desde_aniversario = (hoje - dia_aniversario).days
        return round(idade + (dias_desde_aniversario / 365.25), 2)
    
    @property
    def elegivel_transicao(self) -> bool:
        if not self.data_filiacao_rgps:
            return False
        data_corte = date(2019, 11, 13)
        return self.data_filiacao_rgps < data_corte
    
    @property
    def tempo_contribuicao_anos(self) -> float:
        return round(self.tempo_contribuicao_dias / 365.25, 2)
