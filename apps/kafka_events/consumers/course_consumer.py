import json

from django.conf import settings
from kafka import KafkaConsumer


def consume_course_created_events():
    try:
        consumer = KafkaConsumer(
            settings.KAFKA_COURSE_TOPIC,
            bootstrap_servers=[settings.KAFKA_BROKER_URL],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='course_created_group'
        )

        print(f"🎯 Escutando eventos no tópico '{settings.KAFKA_COURSE_TOPIC}'...") # noqa501

        for message in consumer:
            course_data = message.value
            print(f"📚 Novo Curso Criado: {course_data['title']} (ID: {course_data['id']})") # noqa501

    except Exception as e:
        print(f"❌ Erro ao consumir eventos de curso: {e}")


if __name__ == "__main__":
    consume_course_created_events()
