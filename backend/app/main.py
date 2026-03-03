from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import cliente
import os
from dotenv import load_dotenv
from datetime import date

# Importar routers diretamente dos arquivos
from app.api.clientes import router as clientes_router
from app.api.analises import router as analises_router
from app.api.auth import router as auth_router
from app.api.admin import router as admin_router
from app.api.documentos import router as documentos_router

load_dotenv()

# Cria as tabelas no banco de dados
cliente.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=os.getenv("PROJECT_NAME", "PrevidênciaFácil API"),
    description="Sistema de Enquadramento Previdenciário Automático",
    version=os.getenv("VERSION", "1.0.0")
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers - sem prefixo adicional pois já têm prefixo definido
app.include_router(clientes_router)
app.include_router(analises_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(documentos_router)

@app.get("/")
def root():
    return {
        "message": "PrevidênciaFácil API - Online",
        "version": os.getenv("VERSION", "1.0.0"),
        "status": "operacional"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": date.today().isoformat(),
        "database": "conectado"
    }

@app.get("/routes")
def list_routes():
    """Lista todas as rotas disponíveis (para debug)"""
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods) if hasattr(route, 'methods') else []
        })
    return routes

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Configurar rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
from app.api.admin import router as admin_router
app.include_router(admin_router)
