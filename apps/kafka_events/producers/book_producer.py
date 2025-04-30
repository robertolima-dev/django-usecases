from django.conf import settings

from apps.kafka_events.utils.resilient_kafka_producer import \
    safe_send_kafka_event


def send_book_created_event(book):
    event = {
        "id": book.id,
        "title": book.title,
        "created_at": str(book.created_at),
    }

    safe_send_kafka_event(settings.KAFKA_COURSE_TOPIC, event)
