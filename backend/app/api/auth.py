from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import bcrypt
import jwt
import os
from typing import Optional

from app.database import get_db
from app.models.usuario import UsuarioDB

router = APIRouter(prefix="/auth", tags=["Autenticação"])

# Configurações
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login com email e senha - retorna token JWT"""
    
    # Buscar usuário por email
    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.email == form_data.username,
        UsuarioDB.ativo == True
    ).first()
    
    # Verificar se usuário existe e senha está correta
    if not usuario or not bcrypt.checkpw(
        form_data.password.encode('utf-8'),
        usuario.senha_hash.encode('utf-8')
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Atualizar último acesso
    usuario.ultimo_acesso = datetime.utcnow()
    db.commit()
    
    # Criar token
    access_token = create_access_token(
        data={
            "sub": str(usuario.id),
            "escritorio_id": str(usuario.escritorio_id),
            "email": usuario.email,
            "nome": usuario.nome
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id": str(usuario.id),
            "nome": usuario.nome,
            "email": usuario.email,
            "escritorio_id": str(usuario.escritorio_id),
            "is_admin": usuario.is_admin
        }
    }

@router.post("/registro")
async def registro(
    nome: str,
    email: str,
    senha: str,
    nome_escritorio: str,
    db: Session = Depends(get_db)
):
    """Registro de novo escritório e usuário admin"""
    
    # Verificar se email já existe
    if db.query(UsuarioDB).filter(UsuarioDB.email == email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Criar escritório
    from app.models.usuario import EscritorioDB
    escritorio = EscritorioDB(
        nome=nome_escritorio,
        plano="gratuito"
    )
    db.add(escritorio)
    db.flush()
    
    # Criar hash da senha
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Criar usuário admin
    usuario = UsuarioDB(
        escritorio_id=escritorio.id,
        nome=nome,
        email=email,
        senha_hash=senha_hash,
        is_admin=True,
        ativo=True
    )
    db.add(usuario)
    db.commit()
    
    return {"mensagem": "Escritório criado com sucesso", "id": str(escritorio.id)}

@router.get("/me")
async def me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Dados do usuário logado"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == usuario_id,
        UsuarioDB.ativo == True
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    return {
        "id": str(usuario.id),
        "nome": usuario.nome,
        "email": usuario.email,
        "escritorio_id": str(usuario.escritorio_id),
        "is_admin": usuario.is_admin
    }
