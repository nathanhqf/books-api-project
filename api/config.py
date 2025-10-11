"""
Configurações da API

Contém todas as configurações e constantes da aplicação.
"""

from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho para o arquivo CSV com os dados
DATA_PATH = BASE_DIR / "data" / "books.csv"

# Configurações da API
API_TITLE = "Books API - Tech Challenge"
API_VERSION = "1.0.0"
API_DESCRIPTION = """
API pública para consulta de livros extraídos de Books to Scrape.

## Funcionalidades

* **Consulta de Livros**: Liste todos os livros ou busque por ID
* **Busca Avançada**: Pesquise por título e/ou categoria
* **Categorias**: Liste todas as categorias disponíveis
* **Estatísticas**: Obtenha insights sobre a coleção de livros
* **Health Check**: Verifique o status da API

## Desenvolvido para

Tech Challenge - Fase 1 - Machine Learning Engineering

Projeto completo com web scraping, API REST e boas práticas de desenvolvimento.
"""

# Configurações de paginação
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
