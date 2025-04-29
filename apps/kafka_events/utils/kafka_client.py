import json

from django.conf import settings
from kafka import KafkaProducer


def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=[settings.KAFKA_BROKER_URL],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
