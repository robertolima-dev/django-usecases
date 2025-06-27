import json

from django.conf import settings
from kafka import KafkaConsumer

USE_KAFKA = settings.PROJECT_ENV == "develop_local"


def consume_book_created_events():

    if not USE_KAFKA:
        exit()

    try:
        consumer = KafkaConsumer(
            settings.KAFKA_BOOK_TOPIC,
            bootstrap_servers=[settings.KAFKA_BROKER_URL],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='book_created_group'
        )

        print(f"🎯 Escutando eventos no tópico '{settings.KAFKA_BOOK_TOPIC}'...")  # noqa: E501

        for message in consumer:
            book_data = message.value
            print(f"📚 Novo Livro Criado: {book_data['title']} (ID: {book_data['id']})")  # noqa: E501

    except Exception as e:
        print(f"❌ Erro ao consumir eventos de livro: {e}")


if __name__ == "__main__":
    consume_book_created_events()
