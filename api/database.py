"""
Módulo de Acesso aos Dados

Gerencia o carregamento e consulta dos dados dos livros.
Refatorado para não depender de pandas (reduz bundle no Vercel).
"""

import csv
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
        self.records = []  # type: List[Dict]
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
            
            # Lê o CSV usando csv.DictReader
            with self.csv_path.open(newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = []
                for row in reader:
                    try:
                        # Conversões de tipos
                        row['id'] = int(row.get('id', 0))
                        price_val = row.get('price', '0')
                        if isinstance(price_val, str):
                            price_val = price_val.replace('£', '').strip()
                        row['price'] = float(price_val) if price_val else 0.0
                        row['rating'] = int(row.get('rating', 0))
                        # Padronizar availability
                        avail = row.get('availability', '')
                        row['availability'] = 'In Stock' if 'in stock' in avail.lower() else 'Out of Stock'
                        row['title'] = row.get('title', '')
                        row['category'] = row.get('category', '')
                        data.append(row)
                    except Exception:
                        continue  # Ignora linhas malformadas
            
            self.records = data
            print(f"✓ Dados carregados: {len(self.records)} livros")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return False
    
    def is_loaded(self) -> bool:
        """Verifica se os dados estão carregados"""
        return bool(self.records)
    
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
        
        return self.records[skip:skip + limit]
    
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
        
        for book in self.records:
            if book.get('id') == book_id:
                return book
        return None
    
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
        
        filtered = self.records
        
        if title:
            filtered = [b for b in filtered if title.lower() in b.get('title', '').lower()]
        
        if category:
            filtered = [b for b in filtered if category.lower() in b.get('category', '').lower()]
        
        return filtered[skip:skip + limit]
    
    def get_all_categories(self) -> List[str]:
        """Retorna lista de todas as categorias únicas"""
        if not self.is_loaded():
            return []
        
        categories = {b.get('category', '') for b in self.records if b.get('category')}
        return sorted(categories)
    
    def get_total_count(self) -> int:
        """Retorna o número total de livros"""
        if not self.is_loaded():
            return 0
        return len(self.records)
    
    def get_stats_overview(self) -> Dict:
        """Retorna estatísticas gerais da coleção"""
        if not self.is_loaded():
            return {}
        
        prices = [b['price'] for b in self.records if isinstance(b.get('price'), (int, float))]
        ratings = [b['rating'] for b in self.records if isinstance(b.get('rating'), (int, float))]
        categories = {b.get('category') for b in self.records if b.get('category')}
        in_stock = sum(1 for b in self.records if b.get('availability') == 'In Stock')
        out_stock = sum(1 for b in self.records if b.get('availability') == 'Out of Stock')
        
        return {
            "total_books": len(self.records),
            "total_categories": len(categories),
            "average_price": round(sum(prices) / len(prices), 2) if prices else 0.0,
            "min_price": round(min(prices), 2) if prices else 0.0,
            "max_price": round(max(prices), 2) if prices else 0.0,
            "average_rating": round(sum(ratings) / len(ratings), 2) if ratings else 0.0,
            "in_stock_count": in_stock,
            "out_of_stock_count": out_stock
        }
    
    def get_stats_by_category(self) -> List[Dict]:
        """Retorna estatísticas por categoria"""
        if not self.is_loaded():
            return []
        
        # Agrupa por categoria
        grouped = {}
        for b in self.records:
            cat = b.get('category', '')
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(b)
        
        results = []
        for cat, books in grouped.items():
            prices = [b['price'] for b in books if isinstance(b.get('price'), (int, float))]
            ratings = [b['rating'] for b in books if isinstance(b.get('rating'), (int, float))]
            
            results.append({
                'category': cat,
                'count': len(books),
                'avg_price': round(sum(prices) / len(prices), 2) if prices else 0.0,
                'min_price': round(min(prices), 2) if prices else 0.0,
                'max_price': round(max(prices), 2) if prices else 0.0,
                'avg_rating': round(sum(ratings) / len(ratings), 2) if ratings else 0.0,
            })
        
        # Ordena por count decrescente
        results.sort(key=lambda x: x['count'], reverse=True)
        return results
    
    def get_top_rated_books(self, limit: int = 10) -> List[Dict]:
        """Retorna os livros com melhor avaliação"""
        if not self.is_loaded():
            return []
        
        top_books = [b for b in self.records if b.get('rating') == 5]
        top_books.sort(key=lambda x: x.get('title', ''))
        return top_books[:limit]
    
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
        
        filtered = [
            b for b in self.records 
            if isinstance(b.get('price'), (int, float)) and min_price <= b['price'] <= max_price
        ]
        return filtered[skip:skip + limit]


# Instância global do banco de dados (singleton)
db = BooksDatabase()

