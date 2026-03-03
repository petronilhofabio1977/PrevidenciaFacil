import sys
import os
import uuid
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.cliente import Usuario

db = SessionLocal()

# Verificar se já existe usuário
usuario = db.query(Usuario).first()
if not usuario:
    # Criar usuário padrão
    usuario = Usuario(
        id=uuid.uuid4(),
        nome="Administrador",
        email="admin@previdenci facil.com",
        senha_hash="senha_hash_aqui",  # Depois implementar hash
        criado_em=datetime.now(),
        ativo=True
    )
    db.add(usuario)
    db.commit()
    print(f"✅ Usuário criado com ID: {usuario.id}")
else:
    print(f"✅ Usuário já existe com ID: {usuario.id}")

db.close()
