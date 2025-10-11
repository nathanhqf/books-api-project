"""
Router de Health Check
"""

from fastapi import APIRouter
from api.models.schemas import HealthResponse
from api.config import API_VERSION
from api.database import db

router = APIRouter(prefix="/api/v1", tags=["Health"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Verifica o status da API e conectividade com os dados"""
    data_loaded = db.is_loaded()
    total_books = db.get_total_count() if data_loaded else 0
    
    if data_loaded:
        status = "healthy"
        message = f"API funcionando corretamente. {total_books} livros disponíveis."
    else:
        status = "degraded"
        message = "API funcionando, mas dados não estão carregados."
    
    return HealthResponse(
        status=status,
        api_version=API_VERSION,
        data_loaded=data_loaded,
        total_books=total_books,
        message=message
    )
