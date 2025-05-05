# Integração Elasticsearch com Django (`django-usecases`)

Este guia mostra como integrar e utilizar Elasticsearch com Django e Django REST Framework no projeto [django-usecases](https://github.com/robertolima-dev/django-usecases), incluindo buscas lexicais, autocompletar e buscas semânticas.

---

## ✅ 1. Subir Elasticsearch com Docker

```bash
docker run -d -p 9200:9200 --name elasticsearch -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.11.1
```

---

## ✅ 2. Instalar dependências

```bash
pip install elasticsearch django-elasticsearch-dsl
```

---

## ✅ 3. Configurar `settings.py`

```python
ELASTICSEARCH_DSL = {
    "default": {
        "hosts": "http://localhost:9200"
    }
}
```

---

## ✅ 4. Criar um documento para indexação

`apps/course/documents.py`:

```python
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from apps.course.models import Course

@registry.register_document
class CourseDocument(Document):
    class Index:
        name = "courses"

    class Django:
        model = Course
        fields = ["id", "title", "description", "price", "is_active", "created_at"]
```

---

## ✅ 5. Popular o índice

```bash
python manage.py search_index --create
python manage.py search_index --populate
```

---

## ✅ 6. Realizar buscas na view

```python
from apps.course.documents import CourseDocument
from elasticsearch_dsl.query import Q

s = CourseDocument.search()
s = s.query(Q("multi_match", query="django", fields=["title", "description"]))
results = s.execute()
```

---

## ✅ 7. Autocomplete com analisadores

```python
from django_elasticsearch_dsl import analyzer, token_filter

autocomplete_analyzer = analyzer(
    'autocomplete',
    tokenizer="standard",
    filter=["lowercase", token_filter("edge_ngram_filter", type="edge_ngram", min_gram=1, max_gram=20)],
)
```

---

## ✅ 8. Facetas (agregações)

```python
s.aggs.bucket("price_ranges", "range", field="price", ranges=[
    {"to": 50},
    {"from": 50, "to": 150},
    {"from": 150}
])
```

---

## ✅ 9. Busca semântica com Dense Vector

- Utiliza `dense_vector` + `cosineSimilarity`
- Usa `sentence-transformers` localmente para gerar embeddings
- Índice dedicado: `semantic_books`

```json
{
  "query": {
    "script_score": {
      "query": { "match_all": {} },
      "script": {
        "source": "cosineSimilarity(params.query_vector, 'title_vector') + 1.0",
        "params": {
          "query_vector": [0.1, 0.2, ...]
        }
      }
    }
  }
}
```

---

## ✅ Pronto!

Elasticsearch está integrado com Django para buscas lexicais, autocompletar e semântica! 🚀