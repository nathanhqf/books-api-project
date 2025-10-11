"""
Modelos Pydantic para Validação de Dados

Define os schemas para validação de entrada e saída da API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class Book(BaseModel):
    """Modelo de um livro"""
    id: int = Field(..., description="ID único do livro")
    title: str = Field(..., description="Título do livro")
    price: float = Field(..., description="Preço do livro em libras (£)")
    rating: int = Field(..., ge=0, le=5, description="Avaliação do livro (0-5 estrelas)")
    availability: str = Field(..., description="Disponibilidade (In Stock / Out of Stock)")
    category: str = Field(..., description="Categoria do livro")
    image_url: str = Field(..., description="URL da imagem de capa")
    book_url: str = Field(..., description="URL da página do livro")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "A Light in the Attic",
                "price": 51.77,
                "rating": 3,
                "availability": "In Stock",
                "category": "Poetry",
                "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg",
                "book_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
            }
        }


class BooksListResponse(BaseModel):
    """Resposta para lista de livros com paginação"""
    total: int = Field(..., description="Número total de livros")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")
    books: List[Book] = Field(..., description="Lista de livros")


class CategoryResponse(BaseModel):
    """Resposta para lista de categorias"""
    total: int = Field(..., description="Número total de categorias")
    categories: List[str] = Field(..., description="Lista de categorias")


class StatsOverview(BaseModel):
    """Estatísticas gerais da coleção"""
    total_books: int = Field(..., description="Total de livros")
    total_categories: int = Field(..., description="Total de categorias")
    average_price: float = Field(..., description="Preço médio")
    min_price: float = Field(..., description="Preço mínimo")
    max_price: float = Field(..., description="Preço máximo")
    average_rating: float = Field(..., description="Avaliação média")
    in_stock_count: int = Field(..., description="Livros em estoque")
    out_of_stock_count: int = Field(..., description="Livros fora de estoque")


class CategoryStats(BaseModel):
    """Estatísticas de uma categoria"""
    category: str = Field(..., description="Nome da categoria")
    count: int = Field(..., description="Quantidade de livros")
    avg_price: float = Field(..., description="Preço médio")
    min_price: float = Field(..., description="Preço mínimo")
    max_price: float = Field(..., description="Preço máximo")
    avg_rating: float = Field(..., description="Avaliação média")


class HealthResponse(BaseModel):
    """Resposta do health check"""
    model_config = {"protected_namespaces": ()}
    
    status: str = Field(..., description="Status da API")
    api_version: str = Field(..., description="Versão da API")
    data_loaded: bool = Field(..., description="Indica se os dados estão carregados")
    total_books: int = Field(..., description="Total de livros disponíveis")
    message: str = Field(..., description="Mensagem informativa")

