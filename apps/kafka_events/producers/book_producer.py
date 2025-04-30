import logging

from django.conf import settings

from apps.kafka_events.utils.kafka_client import get_kafka_producer

USE_KAFKA = settings.PROJECT_ENV == "develop_local"

producer = get_kafka_producer()
logger = logging.getLogger(__name__)


def send_book_created_event(book):

    if not USE_KAFKA:
        return

    event = {
        "id": book.id,
        "title": book.title,
        "created_at": str(book.created_at),
    }

    try:
        producer.send(settings.KAFKA_BOOK_TOPIC, value=event)
        producer.flush()
        print(f"✅ Evento book_created enviado: {event}")

    except Exception as e:
        logger.error(f"❌ Erro ao enviar evento para Kafka: {e}")
        # Opcional: aqui você poderia adicionar retries, fallback, etc
