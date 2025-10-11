"""
Aplicação Principal FastAPI - Books API

API pública para consulta de livros extraídos via web scraping.
Inclui autenticação JWT, endpoints ML-Ready e monitoramento.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.config import API_TITLE, API_VERSION, API_DESCRIPTION
from api.routers import health, books, categories, stats, auth, scraping
from api.ml import endpoints as ml_endpoints
from api.database import db
from api.monitoring.middleware import log_requests


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    print("API iniciando...")
    if db.is_loaded():
        print(f"Dados carregados: {db.get_total_count()} livros")
    yield
    print("API encerrando...")


# Cria a aplicação FastAPI
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION + "\n\n## 🔐 Autenticação\n\nA API suporta autenticação JWT. Use `/api/v1/auth/login` para obter tokens.\n\n**Credenciais de teste:**\n- Username: `admin` / Password: `admin123`\n- Username: `user` / Password: `user123`",
    lifespan=lifespan
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de monitoramento
app.middleware("http")(log_requests)

# Registra os routers (ordem importa!)
app.include_router(auth.router)  # Autenticação
app.include_router(ml_endpoints.router)  # ML endpoints
app.include_router(stats.router)  # Estatísticas
app.include_router(categories.router)  # Categorias
app.include_router(books.router)  # Livros
app.include_router(health.router)  # Health
app.include_router(scraping.router)  # Scraping


@app.get("/")
async def root():
    """Página inicial da API"""
    return {
        "message": "Books API - Tech Challenge",
        "version": API_VERSION,
        "docs": "/docs",
        "features": {
            "web_scraping": True,
            "jwt_auth": True,
            "ml_ready": True,
            "monitoring": True
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

