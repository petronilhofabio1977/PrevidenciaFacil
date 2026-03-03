from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List

class ClienteBase(BaseModel):
    nome_completo: str
    cpf: str
    data_nascimento: date
    sexo: str
    categoria_segurado: str
    data_filiacao_rgps: Optional[date] = None
    professor: bool = False
    atividade_rural: bool = False
    deficiencia: str = "nenhuma"

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: str  # Agora é string, não UUID
    criado_em: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )
