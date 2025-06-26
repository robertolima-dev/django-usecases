# Projeto Django

## Estudos Avançados com ElasticSearch, Concorrência, Filtros Complexos, Permissões, WebSocket, Logs, Redis, Kafka, SQS, MongoDB, Throttle, Security Headers, Celery Worker, Celery Beat e Circuit Breaker 

Este projeto é um repositório de estudos organizados em 19 apps Django distintos, com foco em soluções reais de performance, concorrência e boas práticas.

## 📁 Estrutura dos Apps

### `book` – Consultas Otimizadas, Comentários, Agregações e Cache Redis
- Modela livros com autor, tags e comentários
- Usa `select_related`, `prefetch_related` e `annotate` para otimizar queries
- Permite filtros por título, autor, tags e número de comentários
- Conta e ordena livros por número de comentários (`comments_count`)
- Utiliza `SerializerMethodField` apenas quando necessário
- **Integração com Cache Redis**:
  - Cacheia listagem de livros (`/books/`) sensível a filtros, ordenação e paginação
  - Cacheia detalhes de livros individuais (`/books/{id}/`)
  - Geração automática de chaves únicas de cache baseadas nos parâmetros da URL
  - Expiração automática dos caches em 5 minutos
  - Invalidação de cache nas operações de criação e atualização de livros
- Comandos para gerar dados fictícios:
  ```bash
  python manage.py populate_books          # Cria livros com tags e autores
  python manage.py populate_comments       # Gera comentários aleatórios
  python manage.py reindex_semantic_books  # Gera indice busca semantica
  ```

### `chat` - sistema de mensagens em tempo real com salas privadas e em grupo
- Salas privadas (1-1) ou em grupo (2+ usuários)
- Envio de mensagens via WebSocket e fallback por API REST
- Histórico completo por sala
- Suporte a diferentes tipos de mensagem (`text`, `image`, `link`, etc.)
- Avatar dos usuários no retorno das mensagens e salas
- Integração com Channels (WebSocket) e Celery (opcional para notificações)

### `ecommerce` - Concorrência e Transações Atômicas
- Simula checkout com ajuste de estoque seguro
- Usa `select_for_update` com `transaction.atomic()`
- Permite testes de concorrência com Celery ou scripts externos
- Integração com `Elasticsearch` via `django-elasticsearch-dsl` somente local
- Indexação automática de produtos ao criar, editar ou remover
- Comando para indexação em massa:  
  ```bash
  python manage.py index_products
  ```

### `report` - Processamento Assíncrono com Celery
- Gera relatórios CSV de usuários ativos
- Executa a geração de arquivos via Celery + Redis
- Atualiza status (`pending`, `processing`, `done`, `failed`)

### `course` - Filtros Avançados, Busca Otimizada e Integração com Elasticsearch
- Filtros completos: textos, datas, números, booleanos e relacionamentos
- Ordenações dinâmicas: order_by=rating, order_by=purchases, ordering=-price, etc.
- **Filtros especiais**: avg_rating_min, min_purchases, only_free, is_featured
- Busca full-text otimizada usando Elasticsearch:
- Busca léxica com multi_match (boost em title)
- Autocomplete inteligente (edge_ngram) no título dos cursos
- Facets dinâmicos (agregações) para categorias, tags e faixas de preço
- Integração flexível local com Elasticsearch apenas em ambiente de desenvolvimento(USE_ELASTIC configurado via settings.PROJECT_ENV)
- Fallback automático para consultas Django ORM em ambientes sem Elasticsearch
- **Notificações em tempo real** para novos cursos publicados, usando WebSocket (Django Channels)

### `permissions` - Sistema de Permissões por Perfil de Acesso
- Baseado no campo `access_level` do model `Profile`
- Permissões com `IsAdmin`, `IsSupport`, `IsUser`, etc.
- Controle de acesso por papel via DRF (`has_permission`)
- Pode ser expandido para RBAC ou ACL no futuro

### `notifications` - Notificações em Tempo Real com WebSocket
- WebSocket com autenticação via token `/ws/notifications/`
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
- Criação de **cotas de uso por tipo de ação** (ex: `upload`)
- Validação automática via `middleware` e/ou `throttle` do DRF
- **Rate Limiting com planos dinâmicos**:
  - `free`: 50 requisições/minuto
  - `pro`: 200 requisições/minuto
  - `admin`: 1000 requisições/minuto
- Implementado via `CustomUserRateThrottle` com base em `user.profile.plan`
- Middleware consulta e bloqueia se limite for atingido
- Armazena consumo diário em `UserQuota` (opcional)
- Reset diário automático (se implementado com cron ou Celery)
- Exemplo prático: limitar **acesso à API pública** ou **operações sensíveis**
- Comando para testar limites via terminal:
  ```bash
  python manage.py test_throttle --token=SEU_TOKEN_JWT
  ```

### `presence` - Presença Online com WebSocket
- WebSocket com autenticação via token `/ws/presence/`
- Rastreia usuários online
- API: `GET /api/v1/online-users/`
- Model `UserPresence`: `user`, `is_online`, `last_seen`

### `dashboard` - Painel Administrativo em Tempo Real
- WebSocket com autenticação via token `/ws/dashboard/`
- Envia dados agregados: total de users, cursos, livros, relatórios
- Atualiza automaticamente ao criar `user`, `course`, `book`, `report` ou `notification`
- Ideal para visualização de métricas sem recarregar a página

### `mailer` - Envio de Emails Assíncronos
- Tecnologias Utilizadas:
  - Celery para tarefas assíncronas
  - Backend SMTP (AWS SES) para envio seguro e confiável
  - Django EmailMessage para construção e envio dos e-mails
  - Banco de Dados para armazenamento dos templates de e-mail

- Funcionalidades:
  - Envio de e-mail para todos os usuários desacoplado via send_email()
  - Integração com templates dinâmicos, permitindo o uso de variáveis no corpo do e-mail
  - Pronto para integração com sistemas de alertas e notificações
  - Cadastro de Books e Courses com notificações automáticas
  - Encadeamento de Tarefas: Chamadas de uma task para outra, como no caso do envio d e-mail para todos os administradores após um evento.

### `image_processing` - Upload e Processamento com Thumbnails
- Upload de imagens vinculado ao usuário autenticado
- **Validação automática** no upload:
  - Formatos permitidos: `JPEG`, `JPG`, `PNG`, `WEBP`
  - Tamanho máximo: 5MB
  - Dimensões mínimas: 300x300 px
- **Processamento assíncrono com Celery** após upload:
  - Geração de 3 tamanhos: `thumbnail` (150x150), `medium` (600px), `large` (1200px)
  - Conversão automática da imagem para `JPEG` ou `WEBP`
- Campo `output_format` para o usuário escolher o formato de saída
- Campos disponíveis:
  - `original_image`, `thumbnail`, `medium`, `large`, `output_format`, `uploaded_at`
- Integração com SQS, não é possível testar localmente.

### `scheduler` – agendamento de tarefas com Celery Beat
- Agendamento automático de tarefas recorrentes com `django-celery-beat`
- Task periódica para **resetar cotas diárias** do app `throttle`
- Execução programada via `CrontabSchedule`
- Integração com Celery Worker e Beat
- Script automatizado no `apps.py` registra a `PeriodicTask` no primeiro load
- Totalmente compatível com ambientes de produção no ECS

### `monitor` – Painel de monitoramento de tarefas Celery no Django Admin
- Visualização completa do histórico de execuções de tarefas Celery
- Exibe: `task_id`, `task_name`, `status`, tempo de execução (`runtime`), data de criação e conclusão
- Filtros por status (`SUCCESS`, `FAILURE`, `PENDING`, etc.) e busca por nome ou ID
- Integração com `django-celery-results`, com backend de resultados armazenados no banco de dados
- Task fallback inteligente: preenche automaticamente o `task_name` se ausente
- Ideal para ambientes com múltiplas workers e tarefas periódicas programadas

### `search` - Busca Semântica Avançada com Elastic e Dense Vectors
- Implementa **busca semântica** baseada em **Dense Vectors** usando `cosine similarity`
- Integração local com **`sentence-transformers`** (`all-MiniLM-L6-v2`) para geração de embeddings
- Utiliza **ElasticSearch 8+** para suporte a `dense_vector` nativo
- Cria um índice dedicado `semantic_books` para armazenar vetores de significado
- **Busca híbrida** combinando:
  - **Semântica** (similaridade de vetores)
  - **Lexical** (`multi_match` textual) com boost no título
- Filtro automático para retornar apenas resultados relevantes (`score ≥ 6.0`)
- APIs disponíveis:
  ```bash
  GET /api/semantic-search/?q=termo_de_busca
  ```

### `kafka_events` - Integração Django com Apache Kafka para Eventos Assíncronos e Resilientes
- Implementa **envio e consumo de eventos Kafka** diretamente do Django
- Configuração dinâmica de **broker** e **tópicos** via `.env` (`KAFKA_BROKER_URL`, `KAFKA_COURSE_TOPIC`)
- **Producer resiliente** com:
  - `retry` com backoff exponencial (`tenacity`)
  - `circuit breaker` com auto-recovery (`pybreaker`)
  - **fallback local**: eventos salvos em disco se Kafka estiver offline
- **Comando para reenviar eventos salvos** em fallback:
  ```bash
  python manage.py resend_kafka_fallback
  ```
- Estrutura modular:
  - **Producers**: envio de eventos por domínio (`course`, `book`)
  - **Consumers**: escutam tópicos de forma desacoplada
  - **Utils**: cliente Kafka, producer resiliente, fallback
- Integração com o app `course` via **Django Signals**
- Fluxo completo com logs e tolerância a falhas
- APIs e comandos disponíveis:
  ```bash
  # Producer interno via Signal
  send_course_created_event(course_instance)

  # Envio manual em lote (teste fila Kafka)
  python manage.py kafka_test

  # Consumer manual
  from kafka_events.consumers.course_consumer import consume_course_created_events
  consume_course_created_events()
  ```

### `knowledge` - Tópicos Avançados para Django Admin
- Modela tópicos com título, descrição, nível (`fundamental`, `intermediate`, `advanced`)
- Admin com coloração dinâmica do campo `nível` usando `format_html`
- Suporte a `inlines` de estudo com o modelo `KnowledgeStudy`
- Registro de estudos realizados por usuários (com notas e data)
- Ações em lote no admin para marcar tópicos como recomendados
- Comando para popular tópicos avançados com `populate_knowledge`
- Comando para simular estudos com usuários via `populate_knowledge_studies`
- Pronto para servir como referência didática ou base para sistema de aprendizado interno

### `security` – Middleware de Segurança com Headers HTTP
- **Proteções ativas com headers HTTP**:
- `X-Frame-Options: DENY` → bloqueia *clickjacking* ao proibir iframes externos
- `X-Content-Type-Options: nosniff` → evita que o navegador interprete arquivos como scripts (MIME sniffing)
- `Strict-Transport-Security: max-age=63072000; includeSubDomains` → força o uso de HTTPS (requer ambiente seguro)
- `Content-Security-Policy: default-src 'self'` → impede carregamento de scripts e recursos de terceiros não autorizados (protege contra XSS)
- **Como testar**:
- Acesse qualquer rota autenticada
- Verifique os headers no navegador (DevTools → Network → Headers) ou via `curl`:
    ```bash
    curl -I http://localhost:8000/
    ```

### `analytics` - Monitoramento de Eventos com MongoDB
- Armazenamento eficiente de eventos usando MongoDB
- Paginação padrão DRF com suporte a grandes volumes de dados
- API REST para listagem e consulta de eventos
- Integração com o projeto Django utilizando o driver pymongo
- Paginação customizada utilizando o padrão LimitOffsetPagination
- Suporte a ordenação por campos específicos


### `mediahub` – Armazenamento de arquivos com suporte a múltiplos providers - Django Storage
* Upload de arquivos de forma desacoplada, segura e escalável
* Suporte a múltiplos storages: **AWS S3** ou **Google Cloud Storage**
* Escolha do provedor via variável de ambiente (`USE_AWS`)
* Geração de nomes de arquivos com **hash único** via `upload_to`
* URLs automáticas compatíveis com CDN (`CloudFront`, `GCP CDN`)
* Extensível para uso de `signed URLs` e integração com cache
* Preparado para produção com **storages externos desacoplados do backend**

### `integrations` – Integração com APIs externas e Logs HTTP
* Cliente HTTP robusto com suporte a **retries automáticos** e **exponencial backoff**
* Registro completo de chamadas HTTP: método, URL, tempo de resposta, status e payload
* Suporte nativo a headers customizados e payloads JSON
* Centraliza interações com serviços externos (ex: OpenAI, APIs públicas, webhooks)
* Armazena falhas para auditoria e facilita troubleshooting
* Integração fácil com `requests` + `Retry` do `urllib3`

---

## ⚙️ Como rodar o projeto

```bash
python -m venv .env
source .env/bin/activate
```

Crie um arquivo venv.sh baseado no venv_example.sh e rode:
```bash
chmod +x venv.sh
source venv.sh
```

```bash
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

## 🚀 Rode o docker compose

```bash
docker-compose up -d
```

## 🚀 Como rodar o Celery + Redis

1. Rode o worker Celery:
```bash
celery -A api_core worker --loglevel=info
```

2. Rode o beat Celery:
```bash
celery -A api_core beat --loglevel=info
```

---
## 🚀 Integração Elasticsearch – Ambiente Local

Este projeto utiliza **Elasticsearch** para otimizar buscas avançadas no app `course`, disponível **apenas em ambiente de desenvolvimento** (`USE_ELASTIC` configurado via `settings.PROJECT_ENV`).

### 📦 Requisitos para uso local

- Docker instalado
- Compose disponível (`docker-compose`)
- Elasticsearch 8.x ou superior

### 🐳 Rodando o Elasticsearch no ambiente local

Para utilizar a busca com Elasticsearch localmente, execute o seguinte comando (apenas uma vez):

```bash
docker run -d \
  --name elastic \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.12.1
```

```bash
curl http://localhost:9200
```

### ⚙️ Configuração no Django

**settings.py**

```python
# Usar Elastic apenas em ambiente local
USE_ELASTIC = PROJECT_ENV == "local"

# Config Elasticsearch
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}
```

### 📚 Comandos Úteis para Gerenciar o Índice

#### 1. Deletar índice
```bash
python manage.py search_index --delete --models course.Course
```

#### 2. Criar índice
```bash
python manage.py search_index --create --models course.Course
```

#### 3. Reindexar cursos
```bash
python manage.py index_courses
```

Esses comandos garantem que o índice `courses` esteja atualizado conforme o `CourseDocument`.

### 🔍 Funcionalidades Ativadas com Elasticsearch

- Busca **full-text** (`multi_match`) com boost para `title`
- **Autocomplete** inteligente com `edge_ngram`
- Fallback automático para consultas ORM caso `USE_ELASTIC = False`

---

## 📝 Documentação da API – `django-usecases`

O projeto está integrado com dois geradores de documentação OpenAPI para APIs REST:

- 🔍 **Swagger UI e ReDoc com drf-spectacular**
- 📄 **Swagger UI com drf-yasg**

### 🔗 Endpoints de documentação

- **drf-spectacular**
  - `/schema/` → OpenAPI JSON
  - `/schema/swagger/` → Swagger UI
  - `/schema/redoc/` → ReDoc

- **drf-yasg**
  - `/swagger/` → Swagger UI
  - `/redoc/` → ReDoc
  - `/swagger.json` → JSON do schema

### ✅ Organização por módulos

Os endpoints estão organizados por aplicação no Swagger e ReDoc através da propriedade `tags`, permitindo fácil navegação por áreas da plataforma:

- `Books` → Endpoints de livros (`/api/v1/books/`)
- `Courses` → Endpoints de cursos (`/api/v1/courses/`)
- `Chat` → Sistema de mensagens privadas (`/api/v1/message/`)
- `Ecommerce` → Produtos e pedidos com controle de estoque (`/api/v1/ecommerce/`)
- `Throttle` → Limites de uso da API (`/api/v1/throttle/`)
- `Scheduler` → Agendamentos periódicos com Celery Beat
- `Image Processing` → Upload e conversão de imagens
- `Monitor` → Painel de tarefas assíncronas com Celery
- ...entre outros módulos

### 🛠️ Anotações nos endpoints

A documentação foi incrementada com:

- `@extend_schema` (`drf-spectacular`) para descrições, exemplos e parâmetros
- `@swagger_auto_schema` (`drf-yasg`) para personalização individual de métodos
- Exemplo de resposta (`OpenApiExample`)
- Parâmetros de consulta (`OpenApiParameter`), como `?ordering=-created_at`


---

## 📚 `search` - Busca Semântica Avançada com Elastic e Dense Vectors

### Exemplo de resposta

```json
[
  {
    "id": 94,
    "title": "Métodos Django",
    "score": 8.92
  },
  {
    "id": 95,
    "title": "Django Queries",
    "score": 8.94
  },
  {
    "id": 96,
    "title": "Django OOP",
    "score": 9.05
  }
]
```

### Tecnologias utilizadas
- ElasticSearch 8.11+
- Kibana 8.11+
- Django REST Framework
- django-elasticsearch-dsl
- sentence-transformers (Hugging Face)

### Comando de reindexação

```bash
python manage.py reindex_semantic_books
```

- Gera embeddings e reindexa todos os livros semanticamente no Elastic.

---

### Casos de uso típicos de retries (integrations)

* 📡 **Chamada a APIs com instabilidade**: como GPT-4 ou serviços externos que demandam tolerância a falhas
* 🔁 **Retentativas seguras** em chamadas que podem retornar 500, 502 ou 429
* 📊 **Observabilidade**: monitoramento de latência e análise de padrões de erro
* 🔐 **Interação com serviços autenticados**, como envio de payloads via `Authorization Bearer`
* 🛠️ **Ambiente de testes**: integração com endpoints de simulação como `httpbin.org` para validação de lógica HTTP
* 🔍 **Auditoria**: armazenar requisições feitas e seus resultados para futura análise, especialmente em operações críticas

---

## 🧩 Design Patterns no projeto `django-usecases`

Este projeto aplica diversos **Design Patterns** clássicos da engenharia de software, tanto de forma implícita (como boas práticas do Django) quanto explicitamente por meio da organização modular, tasks assíncronas e arquitetura desacoplada.

### 1. **Factory Pattern**
- **Onde**: Serializers (`serializer.create()`)
- **Exemplo**: `UploadedImageSerializer`, `CourseSerializer`
- **Descrição**: Os serializers funcionam como fábricas para criação de objetos com lógica de validação e instanciamento encapsulada.

### 2. **Observer Pattern**
- **Onde**: Celery + Django Signals
- **Exemplo**: `create_thumbnail` (task assíncrona), `monitor.signals.fill_task_name_if_missing`
- **Descrição**: Eventos disparam ações subsequentes como notificações ou transformações de dados, desacopladas da lógica principal.

### 3. **Command Pattern**
- **Onde**: `manage.py` custom commands
- **Exemplo**: `python manage.py reset_user_quotas`
- **Descrição**: Lógica encapsulada em comandos reutilizáveis e automatizáveis.

### 4. **Strategy Pattern**
- **Onde**: Filtros dinâmicos, Permissões, WebSocket Consumers
- **Exemplo**: `CourseFilter`, `IsOwnerPermission`, `ChatConsumer`
- **Descrição**: Algoritmos intercambiáveis selecionados em tempo de execução com base no contexto.

### 5. **Proxy Pattern**
- **Onde**: Serializers com campos computados e propriedades em models
- **Exemplo**: `UserMiniSerializer`, `Room.last_message` (no `chat`)
- **Descrição**: Encapsula acesso a objetos complexos com interface simplificada.

---

## 🎯 Decorators personalizados

Este projeto implementa o **Decorator Pattern** para encapsular comportamentos reutilizáveis em torno de views, tasks, actions administrativas e consumers WebSocket.

### ✅ Lista de decorators aplicados

| Decorator | Objetivo | Aplicado em |
|----------|----------|-------------|
| `@log_task_execution` | Loga início/fim/erro de tasks Celery | `image_processing`, `scheduler` |
| `@check_quota(action="...")` | Valida se o usuário tem cota para realizar a ação | `throttle`, `chat`, `upload` |
| `@admin_action_log("msg")` | Registra e notifica actions feitas no Django Admin | `admin.py` de qualquer app |
| `@ensure_room_participant` | Garante que o usuário está em uma `Room` antes de conectar via WebSocket | `chat/consumers.py` |

---

### 📌 Exemplos de uso

#### 📦 `log_task_execution`

```python
@shared_task(name='image_processing.create_thumbnail')
@log_task_execution
def create_thumbnail(image_id):
  pass
```

---

### 💳 App `ecommerce`: concorrência com `select_for_update`

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

### 📊 App `report`: tarefas assíncronas com Celery

### Objetivo:
Gerar relatórios de usuários ativos em background

### Como usar:
- `POST /api/v1/reports/` com payload vazio
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

### 📖 App `book`: consultas com relacionamentos

### Errado:
```python
Book.objects.all()  # causa N+1
```

### Correto:
```python
Book.objects.select_related("author").prefetch_related("tags", "comments").annotate(
    comments_count=Count("comments")
)
```

#### Resposta:
```json
{
  "id": 1,
  "title": "Harry Potter",
  "author": {
    "id": 2,
    "username": "autor"
  },
  "tags": [
    {"id": 1, "name": "Fantasia"},
    {"id": 2, "name": "Magia"}
  ],
  "comments_count": 12
}
```

### Serializer otimizado:
Evite `SerializerMethodField` com queries internas. Use dados pré-carregados ou `annotate()`.

---

### 🚦 App `throttle`: limites de requisições

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

### 🎓 App `course`: filtros avançados e ordenações inteligentes

Listagem de cursos com suporte completo a filtros dinâmicos, relacionamentos e ordenação por popularidade ou avaliação.

### Filtros suportados:
- `title=django` (busca no título)
- `description=avançado` (busca na descrição)
- `price_min=100&price_max=300`
- `start_date_from=2025-04-01&start_date_to=2025-04-30`
- `workload_min=10&workload_max=40`
- `tags=1,3` ou `tag=python`
- `is_active=true`, `is_free=false`, `is_featured=true`
- `category=2`, `instructor=1`
- `avg_rating_min=4` (média mínima de avaliação)
- `min_purchases=10` (mínimo de compras pagas)
- `only_free=true` (gratuitos apenas)

### 📊 Ordenações especiais:

Use o parâmetro `order_by` ou `ordering`:

- `order_by=rating` → cursos com melhor avaliação média
- `order_by=purchases` → cursos mais comprados
- `ordering=-created_at` → mais recentes
- `ordering=-price` → mais caros primeiro

### Exemplo:
```http
GET /api/v1/courses/?price_min=50&tags=1,3&is_free=false&order_by=rating
```

---

### 🔔 App `notifications`: Notificações automáticas:

Ao criar um curso via `POST /api/v1/courses/`, todos os usuários conectados via `/ws/notifications/` recebem notificações em tempo real com o título do curso!

Utilize o wscat para testar no terminal:

```bash
wscat -c "ws://localhost:8000/ws/notifications/?token=TOKEN_DO_USUARIO"
```

---

### 📤 App `image_processing`: Upload de imagem

```http
POST /api/v1/uploads-images/
Authorization: Token SEU_TOKEN

FormData:
- original_image: arquivo (.jpg, .png, .webp, etc.)
- output_format: JPEG ou WEBP (opcional, padrão: JPEG)
```

---

### 👥 App `presence`: lista de presença de usuários online

Uma lista usuários online no `GET /api/v1/online-users/`, todos os usuários conectados via `/ws/presence/` entram numa lista de users online!

Utilize o wscat para conectar um usário:

```bash
wscat -c "ws://localhost:8000/ws/presence/?token=TOKEN_DO_USUARIO"
```
--- 

### 💬 App `chat`: sistema de mensagens em tempo real com salas privadas e em grupo

Envie mensagens entre usuários autenticados em tempo real via WebSocket, com fallback por API REST.

O chat privado é baseado em salas (`Room`) que conectam N usuários.

### 🔧 Como funciona

Crie (ou recupere) uma sala com outro usuário via:

```http
POST /api/v1/rooms/
Authorization: Token TOKEN_DO_USUARIO
{
  "user_ids": [4, 5],
  "name": "Grupo de Estudos"
}
```

```bash
wscat -c "ws://localhost:8000/ws/chat/room/ROOM_ID/?token=TOKEN_DO_USUARIO"
```

Envie uma mensagem assim via websocket:

```json
{
  "type_message": "text",
  "content": {
    "text": "Olá, tudo bem?"
  }
}
```

Enviar mensagens via API REST (opcional):

```http
POST /api/v1/message/send/
Authorization: Token TOKEN_DO_USUARIO
{
  "room_id": 12,
  "type_message": "image",
  "content": {
    "url": "https://meu-bucket.s3.amazonaws.com/foto.jpg",
    "caption": "Foto da reunião"
  }
}
```
---

### 📊 App `dashboard`: Painel Administrativo em Tempo Real

Este app fornece dados agregados de forma dinâmica para um painel administrativo, usando **WebSocket** para envio de informações em tempo real.

### ✅ Casos de Uso

#### 📡 Conexão via WebSocket

O WebSocket do painel administrativo pode ser acessado com:

```bash
wscat -c "ws://localhost:8000/ws/dashboard/?token=TOKEN_DO_USUARIO"
```

#### Resposta:

```json
{
  "type": "dashboard_data",
  "users_count": 51,
  "courses_count": 40,
  "reports_count": 21,
  "books_count": 85
}
```

---

## 📆 Populando dados

```bash
python manage.py populate_users               # Cria 100 usuarios com faker
python manage.py populate_books               # Cria 100 livros aleatórios
python manage.py populate_comments            # Cria comentários aleatórios nos livros
python manage.py populate_courses             # Cria 30 cursos aleatórios
python manage.py populate_rating              # Cria avaliações para cursos
python manage.py populate_payment             # Cria pagamentos de cursos
python manage.py populate_tenants             # Cria tenants com usuários
python manage.py populate_projects            # Cria projetos associados aos tenants
python manage.py populate_rooms_and_messages  # Cria rooms e messages aleatórias
python manage.py reindex_semantic_books       # Cria indice de busca semantica
python manage.py index_courses                # Cria indice de cursos ElasticSearch
python manage.py index_products               # Cria indice de produtos ElasticSearch
python manage.py populate_knowledge           # Cria lista de knowledge
python manage.py populate_knowledge_studies   # Cria alunos para knowledge (inlines)
python manage.py populate_analytics           # Cria 1000 dados no mongodb
```

---

## 📄 Utilidade
Desenvolvido para estudos aprofundados em Django com casos reais e foco em performance, concorrência, boas práticas e comunicação em tempo real.

---

## 🧠 Autor
**Roberto Lima**  
- 📧 **Email**: robertolima.izphera@gmail.com
- 🔗 [GitHub Roberto Lima](https://github.com/robertolima-dev)  
- 💼 [Linkedin Roberto Lima](https://www.linkedin.com/in/roberto-lima-01/)
- 🌐 [Website Roberto Lima](https://robertolima-developer.vercel.app/)
- 👤 [Gravatar Roberto Lima](https://gravatar.com/deliciouslyautomaticf57dc92af0)

