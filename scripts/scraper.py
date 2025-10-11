"""
Web Scraper para Books to Scrape

Este módulo realiza o web scraping do site https://books.toscrape.com/
e extrai informações sobre todos os livros disponíveis.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import time
from pathlib import Path


class BooksScraper:
    """Classe para fazer scraping do site Books to Scrape"""
    
    def __init__(self, base_url: str = "https://books.toscrape.com"):
        """
        Inicializa o scraper.
        
        Args:
            base_url: URL base do site
        """
        self.base_url = base_url
        self.books_data = []
        
    def _get_rating_number(self, rating_class: str) -> int:
        """
        Converte a classe de rating em número.
        
        Args:
            rating_class: Classe CSS do rating (ex: "star-rating Three")
            
        Returns:
            Número de estrelas (1-5)
        """
        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        
        for key in rating_map:
            if key in rating_class:
                return rating_map[key]
        return 0
    
    def _extract_book_info(self, book_element, category: str) -> Dict:
        """
        Extrai informações de um elemento de livro.
        
        Args:
            book_element: Elemento HTML do livro
            category: Categoria do livro
            
        Returns:
            Dicionário com informações do livro
        """
        try:
            # Título
            title = book_element.find('h3').find('a')['title']
            
            # Preço
            price_text = book_element.find('p', class_='price_color').text
            price = float(price_text.replace('£', '').strip())
            
            # Rating
            rating_class = book_element.find('p', class_='star-rating')['class']
            rating = self._get_rating_number(' '.join(rating_class))
            
            # Disponibilidade
            availability = book_element.find('p', class_='instock availability').text.strip()
            in_stock = 'In stock' in availability
            
            # URL da imagem
            img_url = book_element.find('img')['src']
            if img_url.startswith('../'):
                img_url = self.base_url + '/' + img_url.replace('../', '')
            
            # URL do livro
            book_url = book_element.find('h3').find('a')['href']
            if book_url.startswith('../'):
                book_url = self.base_url + '/catalogue/' + book_url.replace('../../../', '')
            
            return {
                'title': title,
                'price': price,
                'rating': rating,
                'availability': 'In Stock' if in_stock else 'Out of Stock',
                'category': category,
                'image_url': img_url,
                'book_url': book_url
            }
        except Exception as e:
            print(f"Erro ao extrair informações do livro: {e}")
            return None
    
    def scrape_category(self, category_url: str, category_name: str) -> List[Dict]:
        """
        Faz scraping de uma categoria específica.
        
        Args:
            category_url: URL da categoria
            category_name: Nome da categoria
            
        Returns:
            Lista de livros da categoria
        """
        books = []
        page = 1
        
        while True:
            # Monta URL da página
            if page == 1:
                url = category_url
            else:
                url = category_url.replace('index.html', f'page-{page}.html')
            
            print(f"  Scraping {category_name} - Página {page}...")
            
            try:
                response = requests.get(url, timeout=10)
                
                # Se a página não existir, termina o loop
                if response.status_code != 200:
                    break
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Encontra todos os livros na página
                book_elements = soup.find_all('article', class_='product_pod')
                
                if not book_elements:
                    break
                
                # Extrai informações de cada livro
                for book_element in book_elements:
                    book_info = self._extract_book_info(book_element, category_name)
                    if book_info:
                        books.append(book_info)
                
                page += 1
                time.sleep(0.5)  # Pausa para não sobrecarregar o servidor
                
            except Exception as e:
                print(f"  Erro ao acessar página {page}: {e}")
                break
        
        return books
    
    def scrape_all_books(self) -> List[Dict]:
        """
        Faz scraping de todos os livros do site.
        
        Returns:
            Lista com todos os livros
        """
        print("\n" + "="*60)
        print("INICIANDO WEB SCRAPING - BOOKS TO SCRAPE")
        print("="*60 + "\n")
        
        all_books = []
        
        try:
            # Acessa a página principal
            print("Acessando página principal...")
            response = requests.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Encontra o menu de categorias
            category_menu = soup.find('ul', class_='nav nav-list').find('ul')
            categories = category_menu.find_all('a')
            
            print(f"✓ Encontradas {len(categories)} categorias\n")
            
            # Itera sobre cada categoria
            for idx, category in enumerate(categories, 1):
                category_name = category.text.strip()
                category_url = self.base_url + '/' + category['href']
                
                print(f"[{idx}/{len(categories)}] Categoria: {category_name}")
                
                # Faz scraping da categoria
                books = self.scrape_category(category_url, category_name)
                all_books.extend(books)
                
                print(f"  ✓ {len(books)} livros encontrados\n")
            
            print("="*60)
            print(f"SCRAPING CONCLUÍDO: {len(all_books)} livros extraídos")
            print("="*60 + "\n")
            
            self.books_data = all_books
            return all_books
            
        except Exception as e:
            print(f"❌ Erro durante o scraping: {e}")
            return []
    
    def save_to_csv(self, filepath: str = "data/books.csv") -> bool:
        """
        Salva os dados em um arquivo CSV.
        
        Args:
            filepath: Caminho do arquivo CSV
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            if not self.books_data:
                print("⚠ Nenhum dado para salvar")
                return False
            
            # Cria o diretório se não existir
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Converte para DataFrame e salva
            df = pd.DataFrame(self.books_data)
            
            # Adiciona ID único para cada livro
            df.insert(0, 'id', range(1, len(df) + 1))
            
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            print(f"✓ Dados salvos em: {filepath}")
            print(f"  Total de livros: {len(df)}")
            print(f"  Colunas: {', '.join(df.columns.tolist())}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar CSV: {e}")
            return False


def main():
    """Função principal para executar o scraper"""
    scraper = BooksScraper()
    books = scraper.scrape_all_books()
    
    if books:
        scraper.save_to_csv("data/books.csv")
    else:
        print("❌ Nenhum livro foi extraído")


if __name__ == "__main__":
    main()
