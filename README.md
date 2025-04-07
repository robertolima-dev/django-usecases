# Projeto Django

## Estudos Avançados com Celery, Concorrência, Filtros, Permissões, WebSocket, Logs e Throttle

Este projeto é um repositório de estudos organizados em 7 apps Django distintos, com foco em soluções reais de performance, concorrência e boas práticas.

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
- **Notificações em tempo real** quando um novo curso é criado, usando WebSocket

### `permissions` - Sistema de Permissões por Perfil de Acesso
- Baseado no campo `access_level` do model `Profile`
- Permissões com `IsAdmin`, `IsSupport`, `IsUser`, etc.
- Controle de acesso por papel via DRF (`has_permission`)
- Pode ser expandido para RBAC ou ACL no futuro

### `notifications` - Notificações em Tempo Real com WebSocket
- WebSocket com autenticação via token (`/ws/notifications/`)
- Suporte a **notificações globais** (`obj_code='platform'`, `obj_id=None`) e **individuais** (`obj_code='user'`, `obj_id=user.id`)
- Broadcast da mensagem para todos os usuários online, mas com **uma única instância persistida**
- Modelos auxiliares:
  - `UserNotificationRead`: marca notificações como lidas por usuário
  - `UserNotificationDeleted`: armazena quais usuários "excluíram" notificações
- Notificações retornadas já indicam se foram lidas (`read: true/false`) e ocultam as que foram marcadas como excluídas
- Integração com `course`: ao criar um novo curso, é disparada uma notificação em tempo real
- Método PATCH para marcar como lida:  
  `PATCH /api/v1/notifications/<id>/mark-as-read/`

### `auditlog` - Sistema de Auditoria e Logs de Eventos
- Captura automaticamente ações de `create`, `update` e `delete`
- Armazena: usuário, modelo afetado, ID, representação e mudanças
- Uso de `signals` genéricos e `model_to_dict` com `DjangoJSONEncoder`
- Visualização somente leitura no Django Admin
- Ideal para rastreabilidade e conformidade de segurança

### `tenants` - Suporte a Multitenancy (multi-clientes)
- Model `Tenant` com vínculo a múltiplos usuários
- Middleware que injeta `request.tenant` automaticamente
- Mixin `TenantQuerysetMixin` para isolamento por queryset
- Exemplo de uso com model `Project`, vinculado ao tenant

### `throttle` - Sistema de Cotas e Limites por Usuário (Rate Limiting)
- Criação de cotas de uso por tipo de ação (ex: `upload`)
- Validação automática via `middleware`
- Armazena consumo diário em `UserQuota`
- Middleware consulta e bloqueia se limite for atingido
- Customização por tipo de ação, quantidade e reset diário
- Exemplo prático: limitar uploads por usuário autenticado

### `presence` - Presença Online com WebSocket
- WebSocket `/ws/presence/`
- Rastreia usuários online
- API: `GET /api/v1/online-users/`
- Model `UserPresence`: `user`, `is_online`, `last_seen`

---

## ⚙️ Como rodar o projeto

```bash
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### Rodar com WebSocket (Daphne):
```bash
daphne api_core.asgi:application
```

> O projeto usa Django Channels com ASGI, necessário para WebSockets.

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
    r = requests.post("http://localhost:8000/api/v1/orders/", headers={"Authorization": f"Bearer {token}"}, json={"product_id": 1, "quantity": 1})
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

## 📖 App `throttle`: limites de requisições

```python
from apps.throttle.utils import check_and_increment_quota


class UploadViewSet(ModelViewSet):
    serializer_class = ReportRequestSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        # função => check_and_increment_quota(request.user, "upload") 
        check_and_increment_quota(request.user, "upload")
        return Response({"message": "Upload feito com sucesso!"}, status=status.HTTP_201_CREATED)
```

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

### 🔔 Notificações automáticas:
Ao criar um curso via `POST /api/v1/courses/`, todos os usuários conectados via `/ws/notifications/` recebem notificações em tempo real com o título do curso!

Utilize o wscat para testar no terminal:

```bash
wscat -c "ws://localhost:8000/ws/notifications/?token=TOKEN_AQUI"
```

---

## 🎓 App `presence`: lista de presença de usuários online
Uma lista usuários online no `GET /api/v1/online-users/`, todos os usuários conectados via `/ws/presence/` entram numa lista de users online!

Utilize o wscat para conectar um usário:

```bash
wscat -c "ws://localhost:8000/ws/presence/?token=TOKEN_AQUI"
```

---

## 📆 Populando dados

```bash
python manage.py populate_courses         # Cria 30 cursos aleatórios
python manage.py populate_tenants         # Cria tenants com usuários
python manage.py populate_projects        # Cria projetos associados aos tenants
```

---

## 📄 Utilidade
Desenvolvido para estudos aprofundados em Django com casos reais e foco em performance, concorrência, boas práticas e comunicação em tempo real.

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
