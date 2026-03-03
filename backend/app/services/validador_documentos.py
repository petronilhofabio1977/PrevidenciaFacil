import hashlib
import os
import re
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class ValidadorDocumentos:
    """Serviço de validação de documentos previdenciários"""
    
    def __init__(self):
        self.regras = self._carregar_regras()
    
    def _carregar_regras(self):
        """Carrega as regras de validação para cada tipo de documento"""
        return {
            "rg": {
                "tamanho_maximo": 5 * 1024 * 1024,  # 5MB
                "extensoes": ["pdf", "jpg", "jpeg", "png"],
            },
            "cpf": {
                "tamanho_maximo": 5 * 1024 * 1024,
                "extensoes": ["pdf", "jpg", "jpeg", "png"],
            },
            "cnis": {
                "tamanho_maximo": 10 * 1024 * 1024,  # 10MB
                "extensoes": ["pdf"],
            },
            "ctps": {
                "tamanho_maximo": 10 * 1024 * 1024,
                "extensoes": ["pdf", "jpg", "jpeg", "png"],
            },
            "ppp": {
                "tamanho_maximo": 20 * 1024 * 1024,
                "extensoes": ["pdf"],
            },
            "holerite": {
                "tamanho_maximo": 5 * 1024 * 1024,
                "extensoes": ["pdf", "jpg", "jpeg", "png"],
            },
        }
    
    def calcular_hash(self, arquivo_path: str) -> str:
        """Calcula hash SHA256 do arquivo para verificar duplicatas"""
        sha256 = hashlib.sha256()
        with open(arquivo_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def validar_arquivo(self, arquivo_path: str, tipo: str) -> Dict:
        """Valida um arquivo com base no tipo de documento"""
        resultado = {
            "valido": True,
            "alertas": [],
            "erros": [],
            "metadados": {}
        }
        
        # Verificar se arquivo existe
        if not os.path.exists(arquivo_path):
            resultado["valido"] = False
            resultado["erros"].append("Arquivo não encontrado")
            return resultado
        
        # Obter regras para o tipo
        regras = self.regras.get(tipo, {})
        
        # Validar tamanho
        tamanho = os.path.getsize(arquivo_path)
        resultado["metadados"]["tamanho"] = tamanho
        
        tamanho_maximo = regras.get("tamanho_maximo", 10 * 1024 * 1024)
        if tamanho > tamanho_maximo:
            resultado["alertas"].append(
                f"Arquivo maior que o recomendado ({tamanho_maximo/1024/1024:.0f}MB)"
            )
        
        # Validar extensão
        extensao = Path(arquivo_path).suffix.lower().replace(".", "")
        resultado["metadados"]["extensao"] = extensao
        
        extensoes_permitidas = regras.get("extensoes", ["pdf"])
        if extensao not in extensoes_permitidas:
            resultado["valido"] = False
            resultado["erros"].append(
                f"Extensão não permitida. Permitidas: {', '.join(extensoes_permitidas)}"
            )
        
        # Calcular hash
        resultado["metadados"]["hash"] = self.calcular_hash(arquivo_path)
        
        return resultado
    
    def verificar_duplicata(self, cliente_id: str, hash_arquivo: str, db) -> bool:
        """Verifica se já existe documento com mesmo hash para o cliente"""
        from app.models.documento import DocumentoDB
        from sqlalchemy.orm import Session
        
        existente = db.query(DocumentoDB).filter(
            DocumentoDB.cliente_id == cliente_id,
            DocumentoDB.hash_arquivo == hash_arquivo
        ).first()
        
        return existente is not None
    
    def recomendar_acoes(self, tipo: str, resultado_validacao: Dict) -> List[str]:
        """Recomenda ações com base no resultado da validação"""
        acoes = []
        
        if not resultado_validacao["valido"]:
            acoes.append("Corrigir os erros apontados e enviar novamente")
        
        if resultado_validacao.get("alertas"):
            for alerta in resultado_validacao["alertas"]:
                if "tamanho" in alerta:
                    acoes.append("Comprimir o arquivo antes de usar")
        
        return acoes
