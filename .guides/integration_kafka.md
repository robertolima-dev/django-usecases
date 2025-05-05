# Integração Kafka com Django (`django-usecases`)

Este guia mostra como integrar o Apache Kafka em um projeto Django real, usando o app `kafka_events` no projeto [django-usecases](https://github.com/robertolima-dev/django-usecases) como exemplo.

---

## ✅ 1. Subir Kafka com Docker Compose

```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

---

## ✅ 2. Instalar a lib no Django

```bash
pip install kafka-python
```

---

## ✅ 3. Configurar variável no `.env`

```
KAFKA_BROKER_URL=localhost:9092
KAFKA_COURSE_TOPIC=course_created
```

No `settings.py`:

```python
KAFKA_BROKER_URL = env.str("KAFKA_BROKER_URL", default="")
KAFKA_COURSE_TOPIC = env.str("KAFKA_COURSE_TOPIC", default="course_created")
```

---

## ✅ 4. Criar Producer

```python
# apps/kafka_events/producers/course_producer.py
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=[settings.KAFKA_BROKER_URL],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_course_created_event(course):
    event = {
        "id": course.id,
        "title": course.title,
        "price": str(course.price),
    }
    producer.send(settings.KAFKA_COURSE_TOPIC, value=event)
```

---

## ✅ 5. Disparar evento via signal

```python
# apps/course/signals.py
@receiver(post_save, sender=Course)
def course_created_handler(sender, instance, created, **kwargs):
    if created:
        send_course_created_event(instance)
```

---

## ✅ 6. Criar Consumer

```python
# apps/kafka_events/consumers/course_consumer.py
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    settings.KAFKA_COURSE_TOPIC,
    bootstrap_servers=[settings.KAFKA_BROKER_URL],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='earliest'
)

def consume_course_created_events():
    for message in consumer:
        event = message.value
        print("📥 Novo curso:", event)
```

---

## ✅ 7. Tolerância a falhas (com fallback)

```python
try:
    producer.send(...)
except KafkaError:
    salvar_evento_localmente_para_retry()
```

---

## ✅ 8. Monitorar tópicos

```bash
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
```

---

## 🧪 Testar envio e consumo

```bash
python manage.py shell
>>> from apps.course.models import Course
>>> from apps.kafka_events.consumers.course_consumer import consume_course_created_events
>>> consume_course_created_events()
```

---

## ✅ Pronto!

Kafka está integrado para eventos assíncronos e escaláveis no Django! 🚀