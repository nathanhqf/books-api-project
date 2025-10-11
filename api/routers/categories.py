"""
Router de Categorias
"""

from fastapi import APIRouter, HTTPException
from api.models.schemas import CategoryResponse
from api.database import db

router = APIRouter(prefix="/api/v1", tags=["Categorias"])

@router.get("/categories", response_model=CategoryResponse)
async def get_categories():
    """Lista todas as categorias de livros disponíveis"""
    if not db.is_loaded():
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    categories = db.get_all_categories()
    
    return CategoryResponse(
        total=len(categories),
        categories=categories
    )
