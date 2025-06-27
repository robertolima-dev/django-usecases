from django.core.management.base import BaseCommand

from apps.knowledge.models import KnowledgeTopic


class Command(BaseCommand):
    help = "Popula a base de dados com tópicos avançados de backend"

    def handle(self, *args, **kwargs):
        topics = [
            ("HTTP e REST", "Dominar métodos HTTP, códigos de status e construção de APIs RESTful.", "fundamental"),  # noqa: E501
            ("WebSockets", "Entender comunicação bidirecional em tempo real entre cliente e servidor.", "advanced"),  # noqa: E501
            ("API Design", "Criar APIs intuitivas, versionadas e bem documentadas.", "intermediate"),  # noqa: E501
            ("Autenticação e Autorização", "Conhecer OAuth2, JWT, RBAC, e controle de acesso seguro.", "intermediate"),  # noqa: E501
            ("Banco de Dados Relacional", "Dominar SQL, modelagem, índices, constraints e normalização.", "fundamental"),  # noqa: E501
            ("Banco de Dados Não Relacional", "Conhecer MongoDB, Redis, Elasticsearch e suas aplicações.", "intermediate"),  # noqa: E501
            ("ORMs e Mapeamento Objeto-Relacional", "Usar ORMs com eficiência, evitando armadilhas como N+1.", "fundamental"),  # noqa: E501
            ("Migrations e Versionamento de Esquema", "Gerenciar mudanças em bancos de dados com segurança.", "intermediate"),  # noqa: E501
            ("Mensageria e Filas", "Trabalhar com Kafka, RabbitMQ, SQS para comunicação assíncrona.", "advanced"),  # noqa: E501
            ("Tasks Assíncronas", "Executar tarefas em background com Celery, RQ ou async/await.", "advanced"),  # noqa: E501
            ("Cache", "Melhorar performance com Redis, Memcached e estratégias como TTL e invalidação.", "intermediate"),  # noqa: E501
            ("Escalabilidade", "Projetar sistemas tolerantes a carga com horizontabilidade e sharding.", "advanced"),  # noqa: E501
            ("Segurança", "Proteger contra XSS, CSRF, SQL Injection, e seguir boas práticas de segurança.", "intermediate"),  # noqa: E501
            ("Testes Automatizados", "Cobrir unidade, integração e testes end-to-end.", "fundamental"),  # noqa: E501
            ("Monitoramento e Logs", "Integrar logs estruturados, rastreamento de erros e métricas.", "intermediate"),  # noqa: E501
            ("Documentação", "Gerar e manter documentação de API (OpenAPI/Swagger).", "fundamental"),  # noqa: E501
            ("Docker e Containers", "Empacotar aplicações e serviços de forma reprodutível.", "fundamental"),  # noqa: E501
            ("CI/CD", "Automatizar testes, builds e deploys com GitHub Actions, GitLab CI, etc.", "intermediate"),  # noqa: E501
            ("Ambientes de Deploy", "Conhecer servidores, Lambdas, Kubernetes, Heroku, etc.", "advanced"),  # noqa: E501
            ("Armazenamento de Arquivos", "Usar S3, GCS ou sistemas distribuídos para arquivos.", "intermediate"),  # noqa: E501
            ("Arquitetura de Software", "Projetar sistemas desacoplados, modulares e escaláveis.", "advanced"),  # noqa: E501
            ("Padrões de Projeto", "Aplicar padrões como Repository, Service Layer, CQRS, etc.", "advanced"),  # noqa: E501
            ("Design Orientado a Domínio (DDD)", "Organizar código com foco em domínio e contexto.", "advanced"),  # noqa: E501
            ("Boas práticas de código", "Manter código limpo, DRY, SOLID e facilmente testável.", "fundamental"),  # noqa: E501
            ("Performance e Otimização", "Identificar gargalos e otimizar queries, algoritmos e uso de memória.", "advanced"),  # noqa: E501
            ("Resiliência e Tolerância a Falhas", "Usar retry, circuit breaker e fallback.", "advanced"),  # noqa: E501
            ("Feature Flags", "Controlar liberação de funcionalidades em produção.", "intermediate"),  # noqa: E501
            ("Observabilidade", "Combinar logs, métricas e traces para diagnosticar problemas.", "advanced"),  # noqa: E501
        ]  # noqa: E501

        for title, desc, level in topics:
            KnowledgeTopic.objects.get_or_create(title=title, defaults={
                "description": desc,
                "level": level,
                "is_recommended": True,
            })

        self.stdout.write(self.style.SUCCESS("✅ Tópicos avançados populados com sucesso."))  # noqa: E501
