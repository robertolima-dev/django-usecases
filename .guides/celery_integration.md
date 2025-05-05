## Integração Celery com Django (`django-usecases`)

Este guia apresenta os passos para integrar o Celery com um projeto Django real, usando o projeto [django-usecases](https://github.com/robertolima-dev/django-usecases) como base. O Celery é usado para executar tarefas assíncronas como envio de e-mails, processamento em segundo plano, cron jobs, entre outros.

---

### ✅ 1. Instalar as dependências

```bash
pip install celery redis django-celery-beat
```

---

### ✅ 2. Criar o arquivo `celery.py` no core do projeto

`api_core/celery.py`:

```python
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_core.settings")

app = Celery("api_core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

---

### ✅ 3. Atualizar o `__init__.py` do core

`api_core/__init__.py`:

```python
from .celery import app as celery_app

__all__ = ["celery_app"]
```

---

### ✅ 4. Configurar o Redis como broker no `settings.py`

```python
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
CELERY_TIMEZONE = "UTC"
```

---

### ✅ 5. Usar o Django-Celery-Beat (agendador)

No `INSTALLED_APPS`:

```python
'django_celery_beat',
```

Depois:

```bash
python manage.py migrate
```

---

### ✅ 6. Criar uma tarefa em um app

Exemplo: `apps/book/tasks.py`

```python
from celery import shared_task
from time import sleep

@shared_task
def slow_task(book_id):
    sleep(5)
    print(f"✅ Processamento assíncrono finalizado para livro {book_id}")
```

---

### ✅ 7. Chamar tarefa via view ou signal

```python
from apps.book.tasks import slow_task

slow_task.delay(book.id)
```

---

### ✅ 8. Rodar os workers e beat

**Worker**:

```bash
celery -A api_core worker --loglevel=info
```

**Beat (agendador de tarefas periódicas)**:

```bash
celery -A api_core beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

### ✅ 9. Exemplo de uso no projeto

O app `scheduler` agenda uma tarefa diária para **resetar cotas de usuários**:

```python
# apps/scheduler/tasks.py
@shared_task
def reset_user_quotas():
    ...
```

E isso é agendado automaticamente no `AppConfig.ready()` com:

```python
from django_celery_beat.models import CrontabSchedule, PeriodicTask
```

---

### 🧪 Teste rápido

```python
from apps.book.tasks import slow_task
slow_task.delay(123)
```

Você verá o log no worker após 5 segundos ✅

---

### ✅ Pronto!

Celery está pronto para escalar tarefas assíncronas no seu projeto Django 🚀