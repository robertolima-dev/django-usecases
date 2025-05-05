# Guia de Uso Avançado do annotate() no Django ORM

Este guia mostra exemplos práticos usando `.annotate()` com os modelos `Book`, `Tag`, `Comment` e `User` no contexto do projeto `django-usecases`.

---

## 📊 1. Contar comentários de um livro

```python
Book.objects.annotate(comments_count=Count("comments"))
```

---

## 📈 2. Soma, média, máximo e mínimo

```python
Book.objects.annotate(
    avg_length=Avg("title__length"),
    total_tags=Count("tags"),
    max_id=Max("id"),
    min_id=Min("id")
)
```

---

## 🧮 3. Expressões matemáticas

```python
from django.db.models import F, ExpressionWrapper, DecimalField

Book.objects.annotate(
    title_length=ExpressionWrapper(
        F("title__length") * 2,
        output_field=DecimalField()
    )
)
```

---

## 🔠 4. Concatenação de strings

```python
from django.db.models import Value
from django.db.models.functions import Concat

Book.objects.annotate(
    display_title=Concat("title", Value(" by "), "author__username")
)
```

---

## 📅 5. Agrupamento por data

```python
from django.db.models.functions import TruncMonth

Book.objects.annotate(month=TruncMonth("created_at")).values("month").annotate(total=Count("id"))
```

---

## ✅ 6. Condicional com Case/When

```python
from django.db.models import Case, When, BooleanField

Book.objects.annotate(
    has_many_comments=Case(
        When(comments__count__gte=5, then=True),
        default=False,
        output_field=BooleanField()
    )
)
```

---

## 👤 7. Agrupar por autor

```python
Book.objects.values("author__username").annotate(total_books=Count("id"))
```

---

## 🏷️ 8. Quantidade de tags por livro

```python
Book.objects.annotate(tag_count=Count("tags"))
```

---

## 💡 Dica: ordene pelo campo anotado

```python
.annotate(comments_count=Count("comments")).order_by("-comments_count")
```

---

## ✅ Pronto!

Você agora domina o uso avançado de `.annotate()` para consultas agregadas, condicionais, matemáticas e agrupamentos no Django ORM 🚀