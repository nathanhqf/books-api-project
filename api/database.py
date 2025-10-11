"""
Módulo de Acesso aos Dados

Gerencia o carregamento e consulta dos dados dos livros.
"""

import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
from api.config import DATA_PATH


class BooksDatabase:
    """Classe para gerenciar o acesso aos dados dos livros"""
    
    def __init__(self, csv_path: Path = DATA_PATH):
        """
        Inicializa o banco de dados.
        
        Args:
            csv_path: Caminho para o arquivo CSV
        """
        self.csv_path = csv_path
        self.df: Optional[pd.DataFrame] = None
        self.load_data()
    
    def load_data(self) -> bool:
        """
        Carrega os dados do CSV.
        
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        try:
            if not self.csv_path.exists():
                print(f"⚠ Arquivo CSV não encontrado: {self.csv_path}")
                return False
            
            self.df = pd.read_csv(self.csv_path)
            print(f"✓ Dados carregados: {len(self.df)} livros")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return False
    
    def is_loaded(self) -> bool:
        """Verifica se os dados estão carregados"""
        return self.df is not None and not self.df.empty
    
    def get_all_books(self, skip: int = 0, limit: int = 20) -> List[Dict]:
        """
        Retorna todos os livros com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de livros
        """
        if not self.is_loaded():
            return []
        
        books_page = self.df.iloc[skip:skip + limit]
        return books_page.to_dict('records')
    
    def get_book_by_id(self, book_id: int) -> Optional[Dict]:
        """
        Retorna um livro específico pelo ID.
        
        Args:
            book_id: ID do livro
            
        Returns:
            Dicionário com dados do livro ou None se não encontrado
        """
        if not self.is_loaded():
            return None
        
        book = self.df[self.df['id'] == book_id]
        
        if book.empty:
            return None
        
        return book.iloc[0].to_dict()
    
    def search_books(
        self, 
        title: Optional[str] = None, 
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Dict]:
        """
        Busca livros por título e/ou categoria.
        
        Args:
            title: Título (ou parte dele) para buscar
            category: Categoria para filtrar
            skip: Número de registros para pular
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de livros que correspondem aos critérios
        """
        if not self.is_loaded():
            return []
        
        result = self.df.copy()
        
        if title:
            result = result[result['title'].str.contains(title, case=False, na=False)]
        
        if category:
            result = result[result['category'].str.contains(category, case=False, na=False)]
        
        result = result.iloc[skip:skip + limit]
        return result.to_dict('records')
    
    def get_all_categories(self) -> List[str]:
        """Retorna lista de todas as categorias únicas"""
        if not self.is_loaded():
            return []
        
        categories = self.df['category'].unique().tolist()
        return sorted(categories)
    
    def get_total_count(self) -> int:
        """Retorna o número total de livros"""
        if not self.is_loaded():
            return 0
        return len(self.df)
    
    def get_stats_overview(self) -> Dict:
        """Retorna estatísticas gerais da coleção"""
        if not self.is_loaded():
            return {}
        
        return {
            "total_books": int(len(self.df)),
            "total_categories": int(self.df['category'].nunique()),
            "average_price": round(float(self.df['price'].mean()), 2),
            "min_price": round(float(self.df['price'].min()), 2),
            "max_price": round(float(self.df['price'].max()), 2),
            "average_rating": round(float(self.df['rating'].mean()), 2),
            "in_stock_count": int((self.df['availability'] == 'In Stock').sum()),
            "out_of_stock_count": int((self.df['availability'] == 'Out of Stock').sum())
        }
    
    def get_stats_by_category(self) -> List[Dict]:
        """Retorna estatísticas por categoria"""
        if not self.is_loaded():
            return []
        
        stats = self.df.groupby('category').agg({
            'id': 'count',
            'price': ['mean', 'min', 'max'],
            'rating': 'mean'
        }).reset_index()
        
        stats.columns = ['category', 'count', 'avg_price', 'min_price', 'max_price', 'avg_rating']
        stats['avg_price'] = stats['avg_price'].round(2)
        stats['min_price'] = stats['min_price'].round(2)
        stats['max_price'] = stats['max_price'].round(2)
        stats['avg_rating'] = stats['avg_rating'].round(2)
        stats = stats.sort_values('count', ascending=False)
        
        return stats.to_dict('records')
    
    def get_top_rated_books(self, limit: int = 10) -> List[Dict]:
        """Retorna os livros com melhor avaliação"""
        if not self.is_loaded():
            return []
        
        top_books = self.df[self.df['rating'] == 5].sort_values('title').head(limit)
        return top_books.to_dict('records')
    
    def get_books_by_price_range(
        self, 
        min_price: float, 
        max_price: float,
        skip: int = 0,
        limit: int = 20
    ) -> List[Dict]:
        """Retorna livros dentro de uma faixa de preço"""
        if not self.is_loaded():
            return []
        
        result = self.df[(self.df['price'] >= min_price) & (self.df['price'] <= max_price)]
        result = result.iloc[skip:skip + limit]
        return result.to_dict('records')


# Instância global do banco de dados (singleton)
db = BooksDatabase()

