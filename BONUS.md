# 🎁 Desafios Bônus - Documentação Detalhada

Este documento detalha a implementação dos três desafios bônus do Tech Challenge.

## 🔐 Desafio 1: Sistema de Autenticação JWT

### Implementação

O sistema de autenticação JWT foi implementado com os seguintes componentes:

#### Arquivos Criados
- `api/auth/jwt_handler.py`: Lógica de criação e validação de tokens
- `api/auth/models.py`: Modelos Pydantic para autenticação
- `api/routers/auth.py`: Endpoints de autenticação

#### Funcionalidades

**1. Login (`POST /api/v1/auth/login`)**
- Autentica usuário com username e password
- Retorna access_token e refresh_token
- Access token expira em 30 minutos
- Refresh token expira em 7 dias

**2. Refresh (`POST /api/v1/auth/refresh`)**
- Renova o access token usando o refresh token
- Retorna novos tokens

**3. Proteção de Rotas**
- Endpoints ML protegidos com `Depends(get_current_user)`
- Requer header `Authorization: Bearer TOKEN`

### Exemplo de Uso

```bash
# 1. Fazer login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Resposta:
# {
#   "access_token": "eyJ...",
#   "refresh_token": "eyJ...",
#   "token_type": "bearer"
# }

# 2. Usar o token para acessar endpoint protegido
curl -X GET http://localhost:8000/api/v1/ml/features \
  -H "Authorization: Bearer eyJ..."

# 3. Renovar token
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"eyJ..."}'
```

### Credenciais de Teste

| Username | Password | Role |
|----------|----------|------|
| admin    | admin123 | admin |
| user     | user123  | user |

---

## 🤖 Desafio 2: Pipeline ML-Ready

### Implementação

Endpoints especializados para integração com pipelines de Machine Learning.

#### Arquivo Criado
- `api/ml/endpoints.py`: Endpoints ML-Ready

#### Endpoints

**1. GET `/api/v1/ml/features`** 🔒
- Retorna metadados sobre as features disponíveis
- Inclui estatísticas descritivas
- Útil para entender os dados antes do treinamento

**Resposta:**
```json
{
  "numeric_features": ["price", "rating"],
  "categorical_features": ["category", "availability"],
  "text_features": ["title"],
  "total_samples": 1000,
  "feature_statistics": {
    "price": {"min": 10.0, "max": 59.99, "mean": 35.07},
    "rating": {"min": 1, "max": 5, "mean": 2.92}
  }
}
```

**2. GET `/api/v1/ml/training-data`** 🔒
- Retorna dados formatados para treinamento
- Parâmetro `limit` para controlar quantidade
- Dados prontos para uso em modelos

**3. POST `/api/v1/ml/predictions`** 🔒
- Endpoint para fazer predições (mock)
- Estrutura preparada para integração com modelo real
- Retorna predição, confiança e versão do modelo

### Exemplo de Uso

```bash
# Obter token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.access_token')

# Obter features
curl -X GET http://localhost:8000/api/v1/ml/features \
  -H "Authorization: Bearer $TOKEN"

# Obter dados de treinamento
curl -X GET "http://localhost:8000/api/v1/ml/training-data?limit=50" \
  -H "Authorization: Bearer $TOKEN"

# Fazer predição
curl -X POST http://localhost:8000/api/v1/ml/predictions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"price": 25.5, "rating": 4, "category": "Fiction"}'
```

### Integração com ML

Estes endpoints podem ser facilmente integrados com:
- **Scikit-learn**: Para treinamento de modelos
- **MLflow**: Para tracking de experimentos
- **TensorFlow/PyTorch**: Para deep learning
- **Airflow**: Para orquestração de pipelines

---

## 📊 Desafio 3: Monitoramento & Analytics

### Implementação

Sistema completo de logs estruturados e monitoramento de requisições.

#### Arquivos Criados
- `api/monitoring/logger.py`: Configuração de logs estruturados
- `api/monitoring/middleware.py`: Middleware de monitoramento

#### Funcionalidades

**1. Logs Estruturados (JSON)**
- Formato JSON para fácil parsing
- Timestamp, nível, mensagem e contexto
- Salvos em `logs/api.log`

**2. Middleware de Monitoramento**
- Registra todas as requisições
- Inclui método, path, status code
- Mede tempo de processamento
- Adiciona header `X-Process-Time` na resposta

### Formato dos Logs

```json
{
  "asctime": "2025-10-11 11:35:30",
  "name": "books_api",
  "levelname": "INFO",
  "message": "Request processed",
  "method": "GET",
  "path": "/api/v1/ml/features",
  "status_code": 200,
  "process_time": 0.005
}
```

### Exemplo de Uso

```bash
# Ver logs em tempo real
tail -f logs/api.log

# Filtrar logs por status code
cat logs/api.log | jq 'select(.status_code >= 400)'

# Calcular tempo médio de resposta
cat logs/api.log | jq '.process_time' | awk '{sum+=$1; count++} END {print sum/count}'

# Contar requisições por endpoint
cat logs/api.log | jq -r '.path' | sort | uniq -c | sort -rn
```

### Análise de Performance

Os logs permitem análises como:
- Identificar endpoints lentos
- Detectar erros frequentes
- Monitorar uso da API
- Gerar relatórios de performance

### Integração com o Streamlit

Para consultar os dados no dashboard, basta rodar no terminal na pasta raiz do projeto o seguinte comando: 
```bash
streamlit run dashboard.py
```

Ao iniciar o servidor do streamlit, basta acessar a URL indicada no terminal e acessar o dashboard.

### Integração com outras Ferramentas

Os logs JSON podem ser facilmente integrados com:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Grafana** + **Loki**
- **Datadog**
- **New Relic**
- **CloudWatch** (AWS)

---

## 🎯 Conclusão

Todos os três desafios bônus foram implementados com sucesso, demonstrando:

1. **Segurança**: Autenticação JWT robusta
2. **Escalabilidade**: Endpoints preparados para ML
3. **Observabilidade**: Logs estruturados e monitoramento

O projeto está pronto para ser usado em produção e facilmente extensível para incluir funcionalidades adicionais.
