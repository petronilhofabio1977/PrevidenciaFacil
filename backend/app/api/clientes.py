from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from app.database import get_db
from app.models.cliente import ClienteDB
from app.models.usuario import UsuarioDB
from app.schemas.cliente import ClienteCreate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])

def get_or_create_default_user(db: Session):
    """Obtém ou cria um usuário padrão para testes"""
    usuario = db.query(UsuarioDB).first()
    if not usuario:
        usuario = UsuarioDB(
            id=uuid.uuid4(),
            nome="Administrador",
            email="admin@previdenci facil.com",
            senha_hash="senha_hash_temporaria",
            criado_em=datetime.now(),
            ativo=True
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
    return usuario

@router.post("/", response_model=ClienteResponse)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Cadastrar novo cliente"""
    try:
        # Garantir que existe um usuário
        usuario = get_or_create_default_user(db)
        
        db_cliente = ClienteDB(
            id=uuid.uuid4(),
            nome_completo=cliente.nome_completo,
            cpf=cliente.cpf,
            data_nascimento=cliente.data_nascimento,
            sexo=cliente.sexo,
            categoria_segurado=cliente.categoria_segurado,
            data_filiacao_rgps=cliente.data_filiacao_rgps,
            professor=cliente.professor,
            atividade_rural=cliente.atividade_rural,
            deficiencia=cliente.deficiencia.upper() if cliente.deficiencia else "NENHUMA",
            observacoes=None,
            criado_em=datetime.now(),
            usuario_id=usuario.id
        )
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        
        return {
            "id": str(db_cliente.id),
            "nome_completo": db_cliente.nome_completo,
            "cpf": db_cliente.cpf,
            "data_nascimento": db_cliente.data_nascimento,
            "sexo": db_cliente.sexo.value if hasattr(db_cliente.sexo, 'value') else db_cliente.sexo,
            "categoria_segurado": db_cliente.categoria_segurado.value if hasattr(db_cliente.categoria_segurado, 'value') else db_cliente.categoria_segurado,
            "data_filiacao_rgps": db_cliente.data_filiacao_rgps,
            "professor": db_cliente.professor,
            "atividade_rural": db_cliente.atividade_rural,
            "deficiencia": db_cliente.deficiencia.value if hasattr(db_cliente.deficiencia, 'value') else db_cliente.deficiencia,
            "criado_em": db_cliente.criado_em
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar cliente: {str(e)}")

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    """Listar todos os clientes"""
    try:
        clientes = db.query(ClienteDB).all()
        return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {str(e)}")

@router.get("/{cliente_id}", response_model=ClienteResponse)
def obter_cliente(cliente_id: str, db: Session = Depends(get_db)):
    """Obter cliente por ID"""
    try:
        cliente_uuid = uuid.UUID(cliente_id)
        cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_uuid).first()
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        return cliente
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar cliente: {str(e)}")

@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(cliente_id: str, cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """Atualizar dados do cliente"""
    try:
        cliente_uuid = uuid.UUID(cliente_id)
        cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_uuid).first()
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        for key, value in cliente_data.dict().items():
            if key == "deficiencia":
                setattr(cliente, key, value.upper())
            else:
                setattr(cliente, key, value)
        
        db.commit()
        db.refresh(cliente)
        return cliente
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(e)}")

@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: str, db: Session = Depends(get_db)):
    """Deletar cliente"""
    try:
        cliente_uuid = uuid.UUID(cliente_id)
        cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_uuid).first()
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        db.delete(cliente)
        db.commit()
        return {"mensagem": "Cliente deletado com sucesso"}
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar cliente: {str(e)}")
