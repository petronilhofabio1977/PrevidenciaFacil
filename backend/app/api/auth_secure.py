from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models.usuario import UsuarioDB

router = APIRouter(prefix="/auth", tags=["Autenticação"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # código existente (vamos manter o original)
    pass

@router.post("/registro")
@limiter.limit("2/hour")
async def registro(
    request: Request,
    nome: str,
    email: str,
    senha: str,
    nome_escritorio: str,
    db: Session = Depends(get_db)
):
    # código existente
    pass
