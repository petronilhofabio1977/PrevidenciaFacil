import uuid
from datetime import datetime
from app.database import SessionLocal
from app.models.documento import DocumentoDB, TipoDocumentoEnum, StatusDocumentoEnum
from app.models.cliente import ClienteDB

db = SessionLocal()

try:
    # Buscar um cliente existente
    cliente = db.query(ClienteDB).first()
    
    if cliente:
        print(f"✅ Cliente encontrado: {cliente.nome_completo}")
        print(f"   ID: {cliente.id}")
        print(f"   CPF: {cliente.cpf}")
        
        # Criar um documento de teste
        documento = DocumentoDB(
            id=uuid.uuid4(),
            cliente_id=cliente.id,
            nome_arquivo="teste_cnis.pdf",
            caminho_arquivo="/tmp/teste_cnis.pdf",
            tipo_documento=TipoDocumentoEnum.CNIS,
            status=StatusDocumentoEnum.PENDENTE,
            tamanho_bytes=1024,
            observacoes="Documento de teste"
        )
        
        db.add(documento)
        db.commit()
        print(f"\n✅ Documento de teste criado com sucesso!")
        print(f"   ID do documento: {documento.id}")
        print(f"   Tipo: {documento.tipo_documento.value}")
        print(f"   Status: {documento.status.value}")
        
        # Listar documentos do cliente
        documentos = db.query(DocumentoDB).filter(
            DocumentoDB.cliente_id == cliente.id
        ).all()
        
        print(f"\n📋 Documentos do cliente ({len(documentos)}):")
        for doc in documentos:
            print(f"   - {doc.nome_arquivo} ({doc.tipo_documento.value}) - {doc.status.value}")
            
    else:
        print("❌ Nenhum cliente encontrado no banco")
        print("   Crie um cliente primeiro usando o endpoint POST /clientes/")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    db.rollback()
finally:
    db.close()
