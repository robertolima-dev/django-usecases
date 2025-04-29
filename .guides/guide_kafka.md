
# 🚀 Guia Rápido: Integração Django + Kafka

## 📦 Instalação

```bash
pip install kafka-python
```

Adicionar no `requirements.txt`:
```
kafka-python>=2.0.2
```

---

## ⚙️ Configurações no .env

```env
KAFKA_BROKER_URL=localhost:9092
KAFKA_COURSE_TOPIC=course_created
```

No `settings.py`:

```python
import os

KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_COURSE_TOPIC = os.getenv("KAFKA_COURSE_TOPIC", "course_created")
```

---

## 🛠️ Estrutura do App kafka_events/

```
kafka_events/
├── utils/
│   └── kafka_client.py
├── producers/
│   └── course_producer.py
├── consumers/
│   └── course_consumer.py
```

---

## 🔥 Kafka Producer - Enviar Evento

Arquivo: `kafka_events/producers/course_producer.py`

```python
from kafka_events.utils.kafka_client import get_kafka_producer
from django.conf import settings
import logging

producer = get_kafka_producer()
logger = logging.getLogger(__name__)

def send_course_created_event(course):
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
```

---

## 🔥 Kafka Consumer - Escutar Evento

Arquivo: `kafka_events/consumers/course_consumer.py`

```python
from kafka import KafkaConsumer
import json
from django.conf import settings

def consume_course_created_events():
    try:
        consumer = KafkaConsumer(
            settings.KAFKA_COURSE_TOPIC,
            bootstrap_servers=[settings.KAFKA_BROKER_URL],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='course_created_group'
        )

        print(f"🎯 Escutando eventos no tópico '{settings.KAFKA_COURSE_TOPIC}'...")

        for message in consumer:
            course_data = message.value
            print(f"📚 Novo Curso Criado: {course_data['title']} (ID: {course_data['id']})")

    except Exception as e:
        print(f"❌ Erro ao consumir eventos de curso: {e}")
```

---

## 📋 Fluxo de Funcionamento

1. Subir Kafka/Zookeeper (`docker-compose up -d`)
2. Rodar Consumer (`python manage.py shell`)
3. Criar um novo Curso (via Admin ou API)
4. Ver o evento sendo processado no console

---

# 🎯 Observações
- Kafka no ambiente local: `localhost:9092`
- Tópico principal: `course_created`
- Extensível para outros eventos facilmente
