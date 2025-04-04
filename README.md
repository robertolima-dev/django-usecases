# Projeto Django - Estudos Avançados com Celery, Concorrência e Filtros

Este projeto é um repositório de estudos organizados em 5 apps Django distintos, com foco em soluções reais de performance, concorrência e boas práticas.

## 📁 Estrutura dos Apps

### `book` - Consultas Otimizadas com Relacionamentos
- Demonstra uso de `select_related` e `prefetch_related`
- Evita problemas de N+1
- Usa `SerializerMethodField` com desempenho aprimorado

### `ecommerce` - Concorrência e Transações Atômicas
- Simula checkout com ajuste de estoque seguro
- Usa `select_for_update` com `transaction.atomic()`
- Permite testes de concorrência com Celery ou scripts externos

### `report` - Processamento Assíncrono com Celery
- Gera relatórios CSV de usuários ativos
- Executa a geração de arquivos via Celery + Redis
- Atualiza status (`pending`, `processing`, `done`, `failed`)

### `course` - Filtros Avançados com Django Filter
- Filtros por textos, datas, números, booleanos, relacionamentos
- Filtros combináveis e ordenação flexível
- Integração com `django-filter` + DRF

### `permissions` - Sistema de Permissões por Perfil de Acesso
- Baseado no campo `access_level` do model `Profile`
- Permissões com `IsAdmin`, `IsSupport`, `IsUser`, etc.
- Controle de acesso por papel via DRF (`has_permission`)
- Pode ser expandido para RBAC ou ACL no futuro

---

## ⚙️ Como rodar o projeto

```bash
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🚀 Como rodar o Celery + Redis

1. Suba o Redis:
```bash
docker run -d -p 6379:6379 --name redis redis
```

2. Rode o worker Celery:
```bash
celery -A api_core worker --loglevel=info
```

---

## 💳 App `ecommerce`: concorrência com `select_for_update`

### Objetivo:
Simular compras simultâneas com ajuste seguro de estoque.

### Testar concorrência:
1. Gere um produto com `stock=1`
2. Use script com threads e dois tokens diferentes:

```python
import threading, requests

def comprar(token):
    r = requests.post("http://localhost:8000/api/orders/", headers={"Authorization": f"Bearer {token}"}, json={"product_id": 1, "quantity": 1})
    print(r.status_code, r.json())

threading.Thread(target=comprar, args=(token1,)).start()
threading.Thread(target=comprar, args=(token2,)).start()
```

### Garantias:
- O primeiro pedido finaliza
- O segundo falha com "Estoque insuficiente"

---

## 📊 App `report`: tarefas assíncronas com Celery

### Objetivo:
Gerar relatórios de usuários ativos em background

### Como usar:
- `POST /api/reports/` com payload vazio
- Task Celery é disparada: `generate_user_report`
- Gera CSV em `media/reports/` e atualiza o campo `file_path`

### Exemplo de resposta:
```json
{
  "status": "done",
  "file_path": "/media/reports/users_report_1.csv"
}
```

---

## 📖 App `book`: consultas com relacionamentos

### Correto:
```python
Book.objects.select_related("author").prefetch_related("tags", "comments")
```

### Errado:
```python
Book.objects.all()  # causa N+1
```

### Serializer otimizado:
Evite `SerializerMethodField` com queries internas. Use dados pré-carregados ou `annotate()`.

---

## 🎓 App `course`: filtros avançados

### Filtros suportados:
- `title=django` (icontains)
- `price_min=100&price_max=300`
- `start_date_from=2025-04-01`
- `tags=1,2`
- `ordering=-created_at`

### Exemplo:
```http
GET /api/courses/?price_min=50&tags=1,3&is_free=false&ordering=-price
```

---

## 📆 Populando dados

```bash
python manage.py populate_courses
```

Cria 30 cursos aleatórios com categorias, tags, instrutores, preços e datas.

---

## 📄 Utilidade
Desenvolvido para estudos aprofundados em Django com casos reais e foco em performance, concorrência e boas práticas.

---

## 🧠 Autor
**Roberto Lima**  
🔗 GitHub: [robertolima-dev](https://github.com/robertolima-dev)  
📧 Email: robertolima.izphera@gmail.com

---

## 💬 **Contato**

- 📧 **Email**: robertolima.izphera@gmail.com
- 💼 **LinkedIn**: [Roberto Lima](https://www.linkedin.com/in/roberto-lima-01/)
- 💼 **Website**: [Roberto Lima](https://robertolima-developer.vercel.app/)
- 💼 **Gravatar**: [Roberto Lima](https://gravatar.com/deliciouslyautomaticf57dc92af0)

