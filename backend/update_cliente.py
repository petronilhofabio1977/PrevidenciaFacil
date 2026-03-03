import re

# Ler o arquivo
with open('app/models/cliente.py', 'r') as f:
    content = f.read()

# Verificar se já tem escritorio_id
if 'escritorio_id' not in content:
    # Adicionar após usuario_id
    pattern = r'(usuario_id = Column\(UUID\(as_uuid=True\), ForeignKey\(\'usuarios.id\'\), nullable=False\))'
    replacement = r'\1\n    escritorio_id = Column(UUID(as_uuid=True), ForeignKey(\'escritorios.id\'), nullable=False)'
    content = re.sub(pattern, replacement, content)

# Adicionar relacionamento após os outros relationships
if 'escritorio = relationship' not in content:
    pattern = r'(periodos_especiais = relationship\("PeriodoEspecialDB", back_populates="cliente", cascade="all, delete-orphan"\))'
    replacement = r'\1\n    escritorio = relationship("EscritorioDB", back_populates="clientes")'
    content = re.sub(pattern, replacement, content)

# Salvar
with open('app/models/cliente.py', 'w') as f:
    f.write(content)

print("✅ Modelo Cliente atualizado com escritorio_id!")
