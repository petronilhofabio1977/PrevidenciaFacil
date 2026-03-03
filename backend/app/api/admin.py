from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models.escritorio import EscritorioDB
from app.models.usuario import UsuarioDB
from app.models.cliente import ClienteDB
from app.models.documento import DocumentoDB
from app.core.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

def verificar_admin(current_user: UsuarioDB = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return current_user

@router.get("/estatisticas")
async def get_estatisticas(
    db: Session = Depends(get_db),
    admin: UsuarioDB = Depends(verificar_admin)
):
    """Estatísticas globais do sistema"""
    
    total_escritorios = db.query(func.count(EscritorioDB.id)).scalar()
    total_usuarios = db.query(func.count(UsuarioDB.id)).scalar()
    total_clientes = db.query(func.count(ClienteDB.id)).scalar()
    total_documentos = db.query(func.count(DocumentoDB.id)).scalar()
    
    return {
        "total_escritorios": total_escritorios,
        "total_usuarios": total_usuarios,
        "total_clientes": total_clientes,
        "total_documentos": total_documentos
    }

@router.get("/escritorios")
async def listar_escritorios(
    db: Session = Depends(get_db),
    admin: UsuarioDB = Depends(verificar_admin)
):
    """Lista todos os escritórios"""
    
    escritorios = db.query(EscritorioDB).all()
    resultado = []
    
    for esc in escritorios:
        total_usuarios = db.query(func.count(UsuarioDB.id)).filter(UsuarioDB.escritorio_id == esc.id).scalar()
        total_clientes = db.query(func.count(ClienteDB.id)).filter(ClienteDB.escritorio_id == esc.id).scalar()
        
        resultado.append({
            "id": str(esc.id),
            "nome": esc.nome,
            "cnpj": esc.cnpj,
            "plano": esc.plano,
            "ativo": esc.ativo,
            "total_usuarios": total_usuarios,
            "total_clientes": total_clientes,
            "data_criacao": esc.data_criacao.isoformat() if esc.data_criacao else None
        })
    
    return resultado
