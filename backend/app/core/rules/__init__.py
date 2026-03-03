from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from app.models.cliente import Cliente

@dataclass
class ResultadoRegra:
    """Resultado da verificação de uma regra previdenciária"""
    nome_regra: str
    elegivel: bool
    rmi_estimada: Optional[float] = None
    o_que_falta: Optional[str] = None
    detalhes: dict = None
    
    def __post_init__(self):
        if self.detalhes is None:
            self.detalhes = {}

class RegraBase(ABC):
    """Classe abstrata base para todas as regras previdenciárias"""
    
    @abstractmethod
    def verificar(self, cliente: Cliente) -> ResultadoRegra:
        """Verifica elegibilidade e retorna resultado completo"""
        pass
    
    @abstractmethod
    def nome(self) -> str:
        """Nome legível da regra para exibição na interface"""
        pass
