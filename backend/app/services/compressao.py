from PIL import Image
import os
from pathlib import Path

class CompressorImagens:
    @staticmethod
    def comprimir(caminho_origem: str, qualidade: int = 85):
        """Comprime imagem mantendo proporções"""
        img = Image.open(caminho_origem)
        
        # Redimensionar se muito grande
        if max(img.size) > 1920:
            img.thumbnail((1920, 1920))
        
        # Salvar com compressão
        caminho_destino = caminho_origem.replace('.', '_compressed.')
        img.save(caminho_destino, optimize=True, quality=qualidade)
        
        # Substituir original pelo comprimido
        os.remove(caminho_origem)
        os.rename(caminho_destino, caminho_origem)
        
        return True
