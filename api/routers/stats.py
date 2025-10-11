"""
Router de Estatísticas
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from api.models.schemas import StatsOverview, CategoryStats, Book
from api.database import db

router = APIRouter(prefix="/api/v1", tags=["Estatísticas"])

@router.get("/stats/overview", response_model=StatsOverview)
async def get_stats_overview():
    """Retorna estatísticas gerais da coleção de livros"""
    if not db.is_loaded():
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    stats = db.get_stats_overview()
    return StatsOverview(**stats)

@router.get("/stats/categories", response_model=List[CategoryStats])
async def get_stats_by_category():
    """Retorna estatísticas detalhadas por categoria"""
    if not db.is_loaded():
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    stats = db.get_stats_by_category()
    return [CategoryStats(**s) for s in stats]

@router.get("/books/top-rated", response_model=List[Book])
async def get_top_rated_books(limit: int = Query(10, ge=1, le=50)):
    """Lista os livros com melhor avaliação (rating 5)"""
    if not db.is_loaded():
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    books = db.get_top_rated_books(limit)
    return [Book(**book) for book in books]

@router.get("/books/price-range", response_model=List[Book])
async def get_books_by_price_range(
    min: float = Query(..., ge=0, description="Preço mínimo"),
    max: float = Query(..., ge=0, description="Preço máximo"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """Filtra livros dentro de uma faixa de preço específica"""
    if not db.is_loaded():
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    if min > max:
        raise HTTPException(status_code=400, detail="Preço mínimo não pode ser maior que o máximo")
    
    books = db.get_books_by_price_range(min, max, skip, limit)
    return [Book(**book) for book in books]
