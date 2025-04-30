
import json
import logging

import pybreaker
from django.conf import settings
from kafka import KafkaProducer
from kafka.errors import KafkaError
from tenacity import retry, stop_after_attempt, wait_exponential

from apps.kafka_events.fallbacks.kafka_fallback import save_event_to_fallback

logger = logging.getLogger(__name__)

USE_KAFKA = settings.PROJECT_ENV == "develop_local"


# 🔔 Listener personalizado para circuit breaker
class KafkaBreakerListener(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        if new_state.name == "open":
            logger.warning("🚨 Circuit Breaker Kafka ABERTO - Kafka desativado temporariamente") # noqa501
        elif new_state.name == "closed":
            logger.info("✅ Circuit Breaker Kafka FECHADO - Kafka voltou ao normal") # noqa501


# ✅ Circuit Breaker com listener
kafka_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=60,
    listeners=[KafkaBreakerListener()]
)

# ✅ Retry: tenta até 3 vezes com backoff exponencial
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)) # noqa501
@kafka_breaker
def safe_send_kafka_event(topic, event):
    if not USE_KAFKA or not settings.KAFKA_BROKER_URL:
        logger.warning("⚠️ Kafka desativado ou mal configurado.")
        return

    try:
        producer = KafkaProducer(
            bootstrap_servers=[settings.KAFKA_BROKER_URL],
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        producer.send(topic, value=event)
        producer.flush()
        logger.info(f"✅ Kafka event sent: {event}")
    except KafkaError as e:
        logger.error(f"❌ Kafka error: {e}")
        save_event_to_fallback(topic, event)
        raise e
    except Exception as ex:
        logger.error(f"❌ Erro inesperado ao enviar evento Kafka: {ex}")
        save_event_to_fallback(topic, event)
        raise ex
