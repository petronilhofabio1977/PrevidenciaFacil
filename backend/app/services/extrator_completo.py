import re
import pdfplumber
import PyPDF2
from datetime import datetime
from typing import Dict, List, Optional, Any
import os
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("⚠️ Tesseract não disponível. OCR limitado.")

class ExtratorDocumentos:
    """Serviço completo para extrair dados de documentos (PDF e imagens)"""
    
    def __init__(self):
        self.config_ocr = '--psm 6 -l por'  # Configuração para português
    
    def extrair(self, caminho_arquivo: str, tipo: str) -> Dict[str, Any]:
        """Extrai dados de qualquer tipo de documento"""
        extensao = Path(caminho_arquivo).suffix.lower()
        
        if extensao == '.pdf':
            return self._processar_pdf(caminho_arquivo, tipo)
        elif extensao in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']:
            return self._processar_imagem(caminho_arquivo, tipo)
        else:
            return {"erro": "Formato não suportado", "dados": {}}
    
    def _processar_pdf(self, caminho: str, tipo: str) -> Dict:
        """Processa PDF e extrai dados"""
        resultado = {
            "tipo": tipo,
            "formato": "pdf",
            "paginas": 0,
            "texto": "",
            "dados": {},
            "alertas": []
        }
        
        try:
            with pdfplumber.open(caminho) as pdf:
                resultado["paginas"] = len(pdf.pages)
                textos = []
                
                for pagina in pdf.pages:
                    texto = pagina.extract_text() or ""
                    textos.append(texto)
                    
                    # Extrair tabelas se houver
                    tabelas = pagina.extract_tables()
                    if tabelas and tipo == "cnis":
                        resultado["dados"]["tabelas"] = tabelas
                
                resultado["texto"] = "\n".join(textos)
                
                # Extração específica por tipo
                if tipo == "cnis":
                    resultado["dados"].update(self._extrair_cnis(resultado["texto"]))
                elif tipo == "ctps":
                    resultado["dados"].update(self._extrair_ctps(resultado["texto"]))
                elif tipo == "ppp":
                    resultado["dados"].update(self._extrair_ppp(resultado["texto"]))
                elif tipo == "holerite":
                    resultado["dados"].update(self._extrair_holerite(resultado["texto"]))
                
        except Exception as e:
            resultado["alertas"].append(f"Erro no PDF: {str(e)}")
        
        return resultado
    
    def _processar_imagem(self, caminho: str, tipo: str) -> Dict:
        """Processa imagem com OCR"""
        resultado = {
            "tipo": tipo,
            "formato": "imagem",
            "texto": "",
            "dados": {},
            "alertas": []
        }
        
        if not TESSERACT_AVAILABLE:
            resultado["alertas"].append("OCR não disponível")
            return resultado
        
        try:
            # Abrir imagem
            imagem = Image.open(caminho)
            
            # Aplicar OCR
            texto = pytesseract.image_to_string(
                imagem, 
                lang='por', 
                config=self.config_ocr
            )
            resultado["texto"] = texto
            
            # Extrair dados específicos
            if tipo == "rg":
                resultado["dados"].update(self._extrair_rg(texto))
            elif tipo == "cpf":
                resultado["dados"].update(self._extrair_cpf(texto))
            elif tipo == "cnis":
                resultado["dados"].update(self._extrair_cnis(texto))
            elif tipo == "ctps":
                resultado["dados"].update(self._extrair_ctps(texto))
            
        except Exception as e:
            resultado["alertas"].append(f"Erro no OCR: {str(e)}")
        
        return resultado
    
    def _extrair_cnis(self, texto: str) -> Dict:
        """Extrai dados do CNIS"""
        dados = {
            "nome": None,
            "cpf": None,
            "nascimento": None,
            "nome_mae": None,
            "vinculos": [],
            "salarios": []
        }
        
        # Nome
        nome_match = re.search(r'N[oO]?[mM][eE]\s*[:\-]?\s*([A-ZÀ-Ú\s]+)', texto, re.IGNORECASE)
        if nome_match:
            dados["nome"] = nome_match.group(1).strip()
        
        # CPF
        cpf_match = re.search(r'CPF\s*[:\-]?\s*([0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2})', texto)
        if cpf_match:
            dados["cpf"] = cpf_match.group(1)
        
        # Data nascimento
        nascimento_match = re.search(r'(\d{2})[\/\-](\d{2})[\/\-](\d{4})', texto)
        if nascimento_match:
            dados["nascimento"] = f"{nascimento_match.group(3)}-{nascimento_match.group(2)}-{nascimento_match.group(1)}"
        
        # Nome da mãe
        mae_match = re.search(r'MÃE[:\s]+([A-ZÀ-Ú\s]+)', texto, re.IGNORECASE)
        if mae_match:
            dados["nome_mae"] = mae_match.group(1).strip()
        
        # Vínculos empregatícios
        vinculos = re.findall(
            r'(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})\s+([A-ZÀ-Ú0-9\s\.\-]+?)\s+([0-9,\.]+)',
            texto, 
            re.MULTILINE
        )
        
        for v in vinculos:
            dados["vinculos"].append({
                "inicio": v[0],
                "fim": v[1],
                "empregador": v[2].strip(),
                "salario": v[3]
            })
        
        return dados
    
    def _extrair_rg(self, texto: str) -> Dict:
        """Extrai dados do RG"""
        dados = {}
        
        rg_match = re.search(r'([0-9]{2}\.?[0-9]{3}\.?[0-9]{3})', texto)
        if rg_match:
            dados["numero"] = rg_match.group(1)
        
        orgao_match = re.search(r'(SSP|PC|SJS|DIC|DGPC|PCMG|ITCP)[\/\-]?([A-Z]{2})', texto, re.IGNORECASE)
        if orgao_match:
            dados["orgao_emissor"] = orgao_match.group(0)
        
        return dados
    
    def _extrair_cpf(self, texto: str) -> Dict:
        """Extrai número do CPF"""
        dados = {}
        cpf_match = re.search(r'([0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2})', texto)
        if cpf_match:
            dados["cpf"] = cpf_match.group(1)
        return dados
    
    def _extrair_ctps(self, texto: str) -> Dict:
        """Extrai dados da CTPS"""
        dados = {
            "numero": None,
            "serie": None,
            "uf": None
        }
        
        ctps_match = re.search(r'([0-9]{6,})', texto)
        if ctps_match:
            dados["numero"] = ctps_match.group(1)
        
        return dados
    
    def _extrair_ppp(self, texto: str) -> Dict:
        """Extrai dados do PPP"""
        dados = {
            "empresa": None,
            "cnpj": None,
            "periodo_inicio": None,
            "periodo_fim": None,
            "agentes_nocivos": []
        }
        
        empresa_match = re.search(r'(?:RAZÃO SOCIAL|EMPRESA)[:\s]+([^\n]+)', texto, re.IGNORECASE)
        if empresa_match:
            dados["empresa"] = empresa_match.group(1).strip()
        
        cnpj_match = re.search(r'CNPJ[:\s]+([0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2})', texto)
        if cnpj_match:
            dados["cnpj"] = cnpj_match.group(1)
        
        return dados
    
    def _extrair_holerite(self, texto: str) -> Dict:
        """Extrai dados do holerite"""
        dados = {
            "empresa": None,
            "funcionario": None,
            "mes_ano": None,
            "salario_base": None,
            "liquido": None
        }
        
        mes_ano_match = re.search(r'(\d{2})/(\d{4})', texto)
        if mes_ano_match:
            dados["mes_ano"] = f"{mes_ano_match.group(1)}/{mes_ano_match.group(2)}"
        
        salario_match = re.search(r'SALÁRIO BASE[:\s]+R?\$?\s*([0-9.,]+)', texto, re.IGNORECASE)
        if salario_match:
            dados["salario_base"] = salario_match.group(1)
        
        return dados
    
    def sugerir_cadastro(self, dados_extraidos: Dict) -> Dict:
        """Sugere atualização do cadastro baseado nos dados extraídos"""
        sugestoes = {}
        
        if dados_extraidos.get("nome"):
            sugestoes["nome_completo"] = dados_extraidos["nome"]
        
        if dados_extraidos.get("cpf"):
            sugestoes["cpf"] = dados_extraidos["cpf"]
        
        if dados_extraidos.get("nascimento"):
            sugestoes["data_nascimento"] = dados_extraidos["nascimento"]
        
        if dados_extraidos.get("vinculos"):
            sugestoes["tempo_contribuicao"] = len(dados_extraidos["vinculos"])
            sugestoes["primeiro_vinculo"] = dados_extraidos["vinculos"][0]["inicio"] if dados_extraidos["vinculos"] else None
        
        return sugestoes
