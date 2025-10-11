# 📚 Books API - Tech Challenge (Versão Completa com Bônus)

API RESTful para consulta de livros, desenvolvida como parte do **Tech Challenge - Fase 1 - Machine Learning Engineering**. O projeto realiza web scraping do site [Books to Scrape](https://books.toscrape.com/) e disponibiliza os dados através de uma API pública construída com FastAPI.

**Esta versão inclui todos os desafios bônus implementados: Autenticação JWT, Pipeline ML-Ready e Monitoramento & Analytics.**

## 🏛️ Arquitetura do Projeto

```
books-api-project/
├── api/
│   ├── main.py              # Aplicação FastAPI principal
│   ├── config.py            # Configurações
│   ├── database.py          # Acesso aos dados (CSV)
│   ├── auth/                # 🔐 Autenticação JWT (Bônus 1)
│   │   ├── jwt_handler.py
│   │   └── models.py
│   ├── ml/                  # 🤖 Endpoints ML-Ready (Bônus 2)
│   │   └── endpoints.py
│   ├── monitoring/          # 📊 Monitoramento (Bônus 3)
│   │   ├── logger.py
│   │   └── middleware.py
│   ├── models/
│   │   └── schemas.py       # Modelos Pydantic
│   └── routers/
│       ├── auth.py          # Rotas de autenticação
│       ├── books.py         # Rotas de livros
│       ├── categories.py    # Rotas de categorias
│       ├── stats.py         # Rotas de estatísticas
│       └── health.py        # Health check
├── data/
│   └── books.csv            # Dados extraídos
├── scripts/
│   └── scraper.py           # Web scraping
├── logs/
│   └── api.log              # Logs estruturados (JSON)
└── requirements.txt
```

## ✨ Funcionalidades

### Funcionalidades Principais
- ✅ **Web Scraping**: Extrai 1000 livros de 50 categorias
- ✅ **API RESTful**: Interface padronizada e documentada
- ✅ **Validação de Dados**: Pydantic para integridade
- ✅ **Documentação Automática**: Swagger UI e ReDoc
- ✅ **Paginação**: Suporte completo em listas
- ✅ **Busca Flexível**: Por título e/ou categoria

### Desafios Bônus Implementados

#### 🔐 Desafio 1: Autenticação JWT
- Sistema completo de autenticação com tokens JWT
- Endpoints `/api/v1/auth/login` e `/api/v1/auth/refresh`
- Proteção de rotas sensíveis (endpoints ML)
- Tokens de acesso (30 min) e refresh (7 dias)

**Credenciais de teste:**
- Admin: `admin` / `admin123`
- User: `user` / `user123`

#### 🤖 Desafio 2: Pipeline ML-Ready
- `/api/v1/ml/features`: Retorna features prontas para ML
- `/api/v1/ml/training-data`: Dados de treinamento formatados
- `/api/v1/ml/predictions`: Endpoint para predições (mock)
- Todos os endpoints protegidos por autenticação

#### 📊 Desafio 3: Monitoramento & Analytics
- Logs estruturados em formato JSON
- Middleware que registra todas as requisições
- Métricas de tempo de processamento
- Logs salvos em `logs/api.log`

## 🚀 Como Executar

### 1. Instalação

```bash
cd books-api-project
pip3 install -r requirements.txt
```

### 2. Coleta de Dados

```bash
python3 scripts/scraper.py
```

### 3. Executando a API

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em `http://localhost:8000`.

## 📚 Documentação da API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints Principais

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| `POST` | `/api/v1/auth/login` | Autentica e retorna tokens JWT | Não |
| `POST` | `/api/v1/auth/refresh` | Renova o token de acesso | Não |
| `GET` | `/api/v1/health` | Status da API | Não |
| `GET` | `/api/v1/books` | Lista todos os livros | Não |
| `GET` | `/api/v1/books/{id}` | Detalhes de um livro | Não |
| `GET` | `/api/v1/books/search` | Busca livros | Não |
| `GET` | `/api/v1/categories` | Lista categorias | Não |
| `GET` | `/api/v1/stats/overview` | Estatísticas gerais | Não |
| `GET` | `/api/v1/ml/features` | Features para ML | **Sim** |
| `GET` | `/api/v1/ml/training-data` | Dados de treinamento | **Sim** |
| `POST` | `/api/v1/ml/predictions` | Fazer predições | **Sim** |
| `POST` | `/api/v1/scraping/trigger` | Dispara o scraping em background e atualiza o CSV | **Sim** (apenas admin) |
| `GET`  | `/api/v1/scraping/status`  | Consulta status da última execução de scraping | **Sim** (apenas admin) |

### Exemplos de Uso

**5. Disparar scraping em background (admin):**
```bash
curl -X POST http://localhost:8000/api/v1/scraping/trigger \
  -H "Authorization: Bearer SEU_TOKEN_ADMIN" 
```

**6. Consultar status do scraping:**
```bash
curl -X GET http://localhost:8000/api/v1/scraping/status \
  -H "Authorization: Bearer SEU_TOKEN_ADMIN" 
```

**1. Fazer login e obter token:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**2. Acessar endpoint protegido:**
```bash
curl -X GET http://localhost:8000/api/v1/ml/features \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**3. Buscar livros:**
```bash
curl -X GET "http://localhost:8000/api/v1/books/search?title=shadow&category=crime"
```

**4. Ver logs estruturados:**
```bash
tail -f logs/api.log
```

## 🎯 Desafios do Tech Challenge

### Requisitos Obrigatórios ✅
- [x] Web scraping de https://books.toscrape.com/
- [x] API REST com FastAPI
- [x] Endpoints de consulta (livros, categorias, busca)
- [x] Dados armazenados em CSV
- [x] Documentação completa
- [x] Código comentado e organizado

### Desafios Bônus ✅
- [x] **Desafio 1**: Sistema de autenticação JWT
- [x] **Desafio 2**: Pipeline ML-Ready com endpoints especializados
- [x] **Desafio 3**: Monitoramento e logs estruturados

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **BeautifulSoup**: Web scraping
- **Pandas**: Manipulação de dados
- **Pydantic**: Validação de dados
- **Python-JOSE**: Tokens JWT
- **Python-JSON-Logger**: Logs estruturados
- **Uvicorn**: Servidor ASGI

## 📈 Próximos Passos

- **Banco de Dados**: Migrar de CSV para PostgreSQL/MongoDB
- **Cache**: Implementar Redis para melhor performance
- **Docker**: Containerizar a aplicação
- **CI/CD**: Pipeline de deploy automatizado
- **ML Real**: Integrar modelos de recomendação reais

## 👨‍💻 Autor

Desenvolvido para o Tech Challenge - Fase 1 - Machine Learning Engineering

---

**Nota**: Este projeto demonstra boas práticas de desenvolvimento de APIs, incluindo autenticação, monitoramento e preparação para integração com pipelines de Machine Learning.

