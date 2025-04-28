
## 📚 Elasticsearch DevTools - Comandos Úteis

### 🛠️ Criação de índice semantic_books com dense_vector
```json
PUT semantic_books
{
  "mappings": {
    "properties": {
      "id": {
        "type": "integer"
      },
      "title": {
        "type": "text"
      },
      "title_vector": {
        "type": "dense_vector",
        "dims": 384,
        "index": true,
        "similarity": "cosine"
      }
    }
  }
}
```

### 🔍 Verificar todos os índices
```bash
GET _cat/indices?v=true
```

### 📚 Consultas em semantic_books

#### Buscar todos os documentos
```bash
GET semantic_books/_search
```

#### Buscar por título (texto "django")
```json
GET semantic_books/_search
{
  "query": {
    "match": {
      "title": "django"
    }
  }
}
```

#### Busca semântica por vetor
```json
GET semantic_books/_search
{
  "query": {
    "script_score": {
      "query": { "match_all": {} },
      "script": {
        "source": "cosineSimilarity(params.query_vector, 'title_vector') + 1.0",
        "params": {
          "query_vector": [0.1, 0.2, -0.1, 0.3, 0.4, 0.5, 0.6, -0.2, 0.7, 0.8]
        }
      }
    }
  }
}
```

#### Deletar documento pelo ID
```bash
DELETE semantic_books/_doc/94
```

#### Atualizar título de um documento
```json
POST semantic_books/_update/94
{
  "doc": {
    "title": "Curso Django Completo"
  }
}
```

#### Criar documento manualmente
```json
POST semantic_books/_doc/999
{
  "id": 999,
  "title": "Curso de Python Básico",
  "title_vector": [0.01, -0.02, 0.88]
}
```

### 📚 Consultas em courses

#### Buscar todos os cursos
```bash
GET courses/_search
```

#### Buscar curso por título "django"
```json
GET courses/_search
{
  "query": {
    "match": {
      "title": "django"
    }
  }
}
```

#### Buscar cursos por múltiplos IDs
```json
GET courses/_search
{
  "query": {
    "terms": {
      "id": [32, 33, 28]
    }
  }
}
```

#### Buscar curso pelo ID diretamente
```bash
GET courses/_doc/32
```

#### Buscar cursos por múltiplos critérios
```json
GET courses/_search
{
  "query": {
    "bool": {
      "must": [
        { "terms": { "id": [11,12,14,15,16,18,19] } },
        { "term": { "is_active": true } },
        { "term": { "category.id": 4 } }
      ]
    }
  }
}
```

#### Buscar cursos criados após 1º Janeiro 2025
```json
GET courses/_search
{
  "query": {
    "range": {
      "created_at": {
        "gte": "2025-01-01T00:00:00Z"
      }
    }
  }
}
```
