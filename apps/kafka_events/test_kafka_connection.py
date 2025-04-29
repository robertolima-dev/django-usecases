import json

from kafka import KafkaProducer


def test_kafka_connection():
    try:
        # Cria o produtor Kafka
        producer = KafkaProducer(
            bootstrap_servers=["localhost:9092"],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # Envia uma mensagem para um tópico de teste
        producer.send('test_topic', value={"message": "Hello Kafka!"})
        producer.flush()

        print("✅ Kafka conectado e mensagem enviada com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao conectar no Kafka: {e}")


if __name__ == "__main__":
    test_kafka_connection()
