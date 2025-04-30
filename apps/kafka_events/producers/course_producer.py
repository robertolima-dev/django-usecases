from django.conf import settings

from apps.kafka_events.utils.resilient_kafka_producer import \
    safe_send_kafka_event


def send_course_created_event(course):
    event = {
        "id": course.id,
        "title": course.title,
        "created_at": str(course.created_at),
    }

    safe_send_kafka_event(settings.KAFKA_COURSE_TOPIC, event)
