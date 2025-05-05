# Integração Redis com Django (`django-usecases`)

Este guia apresenta os passos para integrar o Redis como cache e suporte a workers no projeto [django-usecases](https://github.com/robertolima-dev/django-usecases).

---

## ✅ 1. Instalar Redis localmente

Via Docker:

```bash
docker run -d -p 6379:6379 --name redis redis
```

---

## ✅ 2. Instalar dependências no Django

```bash
pip install redis django-redis
```

---

## ✅ 3. Configurar cache no `settings.py`

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

---

## ✅ 4. Usar cache no código

### 🔹 Cachear queryset

```python
from django.core.cache import cache

def get_books_cached():
    key = "book_list"
    books = cache.get(key)
    if not books:
        books = list(Book.objects.all())
        cache.set(key, books, timeout=60 * 5)
    return books
```

### 🔹 Cachear por chave dinâmica

```python
key = f"course_detail_{course_id}"
```

---

## ✅ 5. Limpar cache

```python
from django.core.cache import cache
cache.clear()
```

---

## ✅ 6. Monitorar chaves no shell

```python
from django.core.cache import cache
client = cache.client.get_client()
client.keys("*")
```

---

## ✅ 7. Interface visual com RedisInsight

```bash
docker run -d -p 8001:8001 --name redisinsight redislabs/redisinsight
```

Acesse em `http://localhost:8001`

---

## ✅ 8. Exemplo no projeto

O app `book` cacheia o resultado de listagens e detalhes com:

```python
cache_key = f"book_detail_{book.id}"
cache.set(cache_key, serializer.data, timeout=3600)
```

E remove com:

```python
cache.delete(f"book_detail_{book.id}")
cache.delete_pattern("book_list_*")
```

---

## ✅ 9. Usar TTL (tempo de vida)

```python
cache.set("key", "value", timeout=60 * 10)  # 10 minutos
```

---

## ✅ Pronto!

Redis está pronto para melhorar performance com cache, workers e filas no seu projeto Django 🚀