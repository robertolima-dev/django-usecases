# Guia de Uso de Subquery e Exists no Django ORM

Este guia apresenta usos práticos e performáticos de `Subquery`, `OuterRef` e `Exists` com os modelos `Book`, `Comment` e `Tag` no projeto `django-usecases`.

---

## ✅ 1. Importações básicas

```python
from django.db.models import Subquery, OuterRef, Exists
```

---

## 🧠 2. Último comentário por livro

```python
from apps.book.models import Comment

latest_comment = Comment.objects.filter(book=OuterRef("pk")).order_by("-created_at")

Book.objects.annotate(
    last_comment_content=Subquery(latest_comment.values("content")[:1])
)
```

---

## ✅ 3. Primeiro tag associada

```python
from apps.book.models import Tag

first_tag = Tag.objects.filter(books=OuterRef("pk")).order_by("id")

Book.objects.annotate(
    first_tag_name=Subquery(first_tag.values("name")[:1])
)
```

---

## 🔍 4. Verificar se um livro tem comentários com `Exists`

```python
pending_comments = Comment.objects.filter(book=OuterRef("pk"), content__icontains="?")

Book.objects.annotate(
    has_pending=Exists(pending_comments)
)
```

---

## 🔁 5. Filtro baseado em Subquery

```python
books_with_python = Book.objects.filter(
    tags__in=Subquery(Tag.objects.filter(name="python").values("id"))
)
```

---

## 🚀 6. Evitar N+1: exemplo prático

```python
books = Book.objects.annotate(
    last_comment=Subquery(
        Comment.objects.filter(book=OuterRef("pk")).order_by("-created_at").values("content")[:1]
    )
)
```

---

## ⚠️ Cuidados

- Subquery precisa sempre de `.values(...)[:1]` para retornar um único valor
- Prefira `annotate()` com `Subquery` quando `join + aggregation` não for suficiente
- Use `Exists()` para checks booleanos, como "tem comentários?"

---

## ✅ Pronto!

Com `Subquery` e `Exists`, você ganha performance, evita N+1 e mantém o código limpo no Django ORM 🚀