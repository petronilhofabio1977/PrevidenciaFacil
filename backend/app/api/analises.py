from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.cliente import ClienteDB
from app.core.engine import MotorPrevidenciario
from app.models.cliente import Cliente

router = APIRouter(prefix="/analises", tags=["Análises"])
motor = MotorPrevidenciario()

@router.post("/{cliente_id}")
def analisar_cliente(cliente_id: str, db: Session = Depends(get_db)):
    """Executar análise de enquadramento"""
    # Buscar cliente no banco
    db_cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Converter para modelo de domínio
    cliente_dominio = Cliente(
        id=str(db_cliente.id),
        nome_completo=db_cliente.nome_completo,
        cpf=db_cliente.cpf,
        data_nascimento=db_cliente.data_nascimento,
        sexo=db_cliente.sexo.value if hasattr(db_cliente.sexo, 'value') else db_cliente.sexo,
        categoria_segurado=db_cliente.categoria_segurado.value if hasattr(db_cliente.categoria_segurado, 'value') else db_cliente.categoria_segurado,
        data_filiacao_rgps=db_cliente.data_filiacao_rgps,
        professor=db_cliente.professor,
        atividade_rural=db_cliente.atividade_rural,
        deficiencia=db_cliente.deficiencia.value if hasattr(db_cliente.deficiencia, 'value') else db_cliente.deficiencia,
        tempo_contribuicao_dias=0,  # Calcular dos vínculos
        salarios_contribuicao=[],    # Buscar do banco
        tem_atividade_especial=False
    )
    
    # Executar análise
    resultados = motor.analisar(cliente_dominio)
    recomendacao = motor.mais_vantajoso(resultados)
    
    return {
        "cliente_id": cliente_id,
        "data_analise": date.today().isoformat(),
        "resultados": [
            {
                "nome_regra": r.nome_regra,
                "elegivel": r.elegivel,
                "rmi_estimada": r.rmi_estimada,
                "o_que_falta": r.o_que_falta,
                "detalhes": r.detalhes
            } for r in resultados
        ],
        "recomendacao": recomendacao.nome_regra if recomendacao else None,
        "motivo": f"Maior RMI: R$ {recomendacao.rmi_estimada:.2f}" if recomendacao else "Nenhuma regra elegível"
    }

@router.get("/{cliente_id}/ultima")
def ultima_analise(cliente_id: str):
    """Buscar última análise do cliente"""
    return {"mensagem": f"Última análise do cliente {cliente_id}"}
