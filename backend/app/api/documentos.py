from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func  # <-- IMPORTANTE: adicionar este import
import uuid
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List

from app.database import get_db
from app.models.cliente import ClienteDB
from app.models.documento import DocumentoDB, TipoDocumentoEnum, StatusDocumentoEnum
from app.services.validador_documentos import ValidadorDocumentos
from app.services.extrator_completo import ExtratorDocumentos

router = APIRouter(prefix="/documentos", tags=["Documentos"])

# Configuração de upload
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads" / "clientes"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Instância dos serviços
validador = ValidadorDocumentos()
extrator = ExtratorDocumentos()

@router.post("/upload/{cliente_id}")
async def upload_documento(
    cliente_id: str,
    tipo: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload com validação, extração e sugestão de cadastro"""
    try:
        # Verificar cliente
        cliente_uuid = uuid.UUID(cliente_id)
        cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_uuid).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        # Criar pasta do cliente
        cliente_nome = cliente.nome_completo.replace(" ", "_").lower()
        cliente_pasta = UPLOAD_DIR / f"{cliente_nome}_{cliente_id[:8]}"
        cliente_pasta.mkdir(exist_ok=True)
        
        # Salvar arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{timestamp}_{file.filename}"
        caminho_completo = cliente_pasta / nome_arquivo
        
        with open(caminho_completo, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # VALIDAÇÃO
        resultado_validacao = validador.validar_arquivo(str(caminho_completo), tipo)
        
        # Verificar duplicata
        hash_arquivo = resultado_validacao["metadados"].get("hash")
        if hash_arquivo and validador.verificar_duplicata(cliente_id, hash_arquivo, db):
            os.remove(caminho_completo)
            raise HTTPException(
                status_code=400, 
                detail="Documento duplicado"
            )
        
        # EXTRAÇÃO DE DADOS
        dados_extraidos = None
        sugestao = None
        
        if resultado_validacao["valido"]:
            resultado_extracao = extrator.extrair(str(caminho_completo), tipo)
            dados_extraidos = resultado_extracao.get("dados", {})
            
            # Sugestão de cadastro
            if dados_extraidos:
                sugestao = extrator.sugerir_cadastro(dados_extraidos)
        
        # Status baseado na validação
        status = StatusDocumentoEnum.VALIDADO.value if resultado_validacao["valido"] else StatusDocumentoEnum.PENDENTE.value
        
        # Criar registro
        documento = DocumentoDB(
            id=uuid.uuid4(),
            cliente_id=cliente_uuid,
            nome_arquivo=file.filename,
            caminho_arquivo=str(caminho_completo),
            tamanho_bytes=resultado_validacao["metadados"].get("tamanho"),
            mime_type=file.content_type,
            hash_arquivo=hash_arquivo,
            tipo_documento=tipo,
            status=status,
            validacao_resultado={
                "validacao": resultado_validacao,
                "dados_extraidos": dados_extraidos,
                "sugestao_cadastro": sugestao
            },
            alertas=resultado_validacao.get("alertas", [])
        )
        
        db.add(documento)
        db.commit()
        db.refresh(documento)
        
        # Resposta
        response = {
            "id": str(documento.id),
            "mensagem": "Documento processado",
            "nome": file.filename,
            "tipo": tipo,
            "status": documento.status,
            "validacao": {
                "valido": resultado_validacao["valido"],
                "alertas": resultado_validacao.get("alertas", [])
            }
        }
        
        if dados_extraidos:
            response["dados_extraidos"] = dados_extraidos
        
        if sugestao:
            response["sugestao_cadastro"] = sugestao
            response["mensagem"] += " - Dados extraídos! Deseja atualizar o cadastro?"
        
        if not resultado_validacao["valido"]:
            response["acoes"] = validador.recomendar_acoes(tipo, resultado_validacao)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@router.get("/cliente/{cliente_id}")
def listar_documentos_cliente(
    cliente_id: str,
    db: Session = Depends(get_db)
):
    """Listar documentos de um cliente"""
    try:
        cliente_uuid = uuid.UUID(cliente_id)
        documentos = db.query(DocumentoDB).filter(
            DocumentoDB.cliente_id == cliente_uuid
        ).order_by(DocumentoDB.data_upload.desc()).all()
        
        return [
            {
                "id": str(doc.id),
                "nome": doc.nome_arquivo,
                "tipo": doc.tipo_documento,
                "status": doc.status,
                "data_upload": doc.data_upload.isoformat() if doc.data_upload else None,
                "alertas": doc.alertas,
                "dados_extraidos": doc.validacao_resultado.get("dados_extraidos") if doc.validacao_resultado else None
            }
            for doc in documentos
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@router.get("/dashboard/validacao")
def dashboard_validacao(
    db: Session = Depends(get_db)
):
    """Dashboard para advogados - documentos pendentes e estatísticas"""
    try:
        # Total de documentos
        total = db.query(DocumentoDB).count()
        
        # Pendentes
        pendentes = db.query(DocumentoDB).filter(
            DocumentoDB.status == StatusDocumentoEnum.PENDENTE.value
        ).count()
        
        # Validados hoje
        hoje = datetime.now().date()
        validados_hoje = db.query(DocumentoDB).filter(
            DocumentoDB.status == StatusDocumentoEnum.VALIDADO.value,
            func.date(DocumentoDB.data_upload) == hoje
        ).count()
        
        # Por tipo de documento
        por_tipo = db.query(
            DocumentoDB.tipo_documento,
            func.count().label('total')
        ).group_by(DocumentoDB.tipo_documento).all()
        
        # Documentos pendentes (para ação)
        docs_pendentes = db.query(DocumentoDB).filter(
            DocumentoDB.status == StatusDocumentoEnum.PENDENTE.value
        ).order_by(DocumentoDB.data_upload).limit(10).all()
        
        return {
            "estatisticas": {
                "total": total,
                "pendentes": pendentes,
                "validados_hoje": validados_hoje
            },
            "por_tipo": [{"tipo": t[0], "total": t[1]} for t in por_tipo],
            "pendentes": [
                {
                    "id": str(d.id),
                    "nome": d.nome_arquivo,
                    "tipo": d.tipo_documento,
                    "data_upload": d.data_upload.isoformat() if d.data_upload else None,
                    "alertas": d.alertas
                }
                for d in docs_pendentes
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@router.post("/cliente/{cliente_id}/atualizar-cadastro")
def atualizar_cadastro_com_documento(
    cliente_id: str,
    documento_id: str,
    db: Session = Depends(get_db)
):
    """Atualiza cadastro do cliente com dados extraídos do documento"""
    try:
        cliente_uuid = uuid.UUID(cliente_id)
        doc_uuid = uuid.UUID(documento_id)
        
        cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_uuid).first()
        documento = db.query(DocumentoDB).filter(DocumentoDB.id == doc_uuid).first()
        
        if not cliente or not documento:
            raise HTTPException(status_code=404, detail="Cliente ou documento não encontrado")
        
        if not documento.validacao_resultado:
            raise HTTPException(status_code=400, detail="Documento sem dados de validação")
        
        dados = documento.validacao_resultado.get("dados_extraidos", {})
        if not dados:
            raise HTTPException(status_code=400, detail="Nenhum dado extraído deste documento")
        
        # Atualizar campos
        campos_atualizados = []
        
        if dados.get("nome") and not cliente.nome_completo:
            cliente.nome_completo = dados["nome"]
            campos_atualizados.append("nome")
            
        if dados.get("cpf") and not cliente.cpf:
            cliente.cpf = dados["cpf"]
            campos_atualizados.append("cpf")
            
        if dados.get("nascimento"):
            try:
                cliente.data_nascimento = datetime.strptime(dados["nascimento"], "%Y-%m-%d").date()
                campos_atualizados.append("data_nascimento")
            except:
                pass
        
        db.commit()
        
        return {
            "mensagem": "Cadastro atualizado com sucesso",
            "campos_atualizados": campos_atualizados
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
