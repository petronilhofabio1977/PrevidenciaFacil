from celery import Celery
from app.services.extrator_completo import ExtratorDocumentos

celery_app = Celery('tasks', broker='redis://redis:6379/0')

@celery_app.task
def processar_ocr(documento_id: str, caminho_arquivo: str):
    """Processa OCR em background"""
    extrator = ExtratorDocumentos()
    resultado = extrator.extrair(caminho_arquivo, 'cnis')
    return resultado
