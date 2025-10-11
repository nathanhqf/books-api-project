"""
Router de Livros

Endpoints principais para consulta de livros.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from api.models.schemas import Book, BooksListResponse
from api.database import db
from api.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

# Cria o router
router = APIRouter(prefix="/api/v1", tags=["Livros"])


@router.get("/books", response_model=BooksListResponse)
async def get_all_books(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Tamanho da página")
):
    """
    Lista todos os livros disponíveis na base de dados com paginação.
    """
    if not db.is_loaded():
        raise HTTPException(status_code=503, detail="Dados não carregados.")
    
    skip = (page - 1) * page_size
    books = db.get_all_books(skip=skip, limit=page_size)
    total = db.get_total_count()
    
    return BooksListResponse(
        total=total,
        page=page,
        page_size=page_size,
        books=[Book(**book) for book in books]
    )


@router.get("/books/search", response_model=BooksListResponse)
async def search_books(
    title: Optional[str] = Query(None, description="Título (ou parte dele) para buscar"),
    category: Optional[str] = Query(None, description="Categoria para filtrar"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Tamanho da página")
):
    """
    Busca livros por título e/ou categoria.
    """
    if not db.is_loaded():
        raise HTTPException(status_code=503, detail="Dados não carregados.")
    
    skip = (page - 1) * page_size
    books = db.search_books(title=title, category=category, skip=skip, limit=page_size)
    all_results = db.search_books(title=title, category=category, skip=0, limit=10000)
    total = len(all_results)
    
    return BooksListResponse(
        total=total,
        page=page,
        page_size=page_size,
        books=[Book(**book) for book in books]
    )


@router.get("/books/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int):
    """
    Retorna detalhes completos de um livro específico pelo ID.
    """
    if not db.is_loaded():
        raise HTTPException(status_code=503, detail="Dados não carregados.")
    
    book = db.get_book_by_id(book_id)
    
    if not book:
        raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado")
    
    return Book(**book)

