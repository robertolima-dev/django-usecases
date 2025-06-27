import json
import logging

from django.conf import settings
from kafka import KafkaProducer

USE_KAFKA = settings.PROJECT_ENV == "develop_local"

logger = logging.getLogger(__name__)


def get_kafka_producer():
    if not USE_KAFKA:
        logger.warning("⚠️ Kafka desabilitado por configuração (USE_KAFKA=False)")  # noqa: E501
        return None

    if not settings.KAFKA_BROKER_URL:
        logger.error("❌ KAFKA_BROKER_URL não definido. Kafka será ignorado.")
        return None

    try:
        producer = KafkaProducer(
            bootstrap_servers=[settings.KAFKA_BROKER_URL],
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        return producer
    except Exception as e:
        logger.error(f"❌ Erro ao criar KafkaProducer: {e}")
        return None
