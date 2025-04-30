import logging

from django.conf import settings

from apps.kafka_events.utils.kafka_client import get_kafka_producer

USE_KAFKA = settings.PROJECT_ENV == "develop_local"

producer = get_kafka_producer()
logger = logging.getLogger(__name__)


def send_course_created_event(course):

    if not USE_KAFKA:
        return

    event = {
        "id": course.id,
        "title": course.title,
        "created_at": str(course.created_at),
    }

    try:
        producer.send(settings.KAFKA_COURSE_TOPIC, value=event)
        producer.flush()
        print(f"✅ Evento course_created enviado: {event}")

    except Exception as e:
        logger.error(f"❌ Erro ao enviar evento para Kafka: {e}")
        # Opcional: aqui você poderia adicionar retries, fallback, etc
