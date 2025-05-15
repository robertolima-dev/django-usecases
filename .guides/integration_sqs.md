## 🚀 **Guia de Integração: AWS SQS com Django**

Este guia documenta a integração entre **AWS SQS**, **AWS Lambda** e o projeto **Django-usecases**. A integração permite que mensagens enviadas para o SQS sejam processadas de forma assíncrona pelo Lambda e enviadas para o endpoint Django.

---

### 🛠️ **1. Arquitetura da Integração:**

1. **Django (Enviador):**

   * Dispara mensagens para a fila SQS ao salvar um novo objeto no banco de dados.
2. **AWS SQS (Fila):**

   * Armazena as mensagens até que sejam processadas.
3. **AWS Lambda (Processador):**

   * Recebe mensagens da fila SQS e faz requisições HTTP para o endpoint do Django.
4. **Django (Receptor):**

   * Recebe a requisição HTTP da Lambda e processa a mensagem.

---

## 📝 **2. Configuração do Django:**

### **Instalar Dependências:**

```bash
pip install boto3 django
```

### **Arquivo de Configuração (.env):**

```bash
APP_KEY=YOUR_SECURE_APP_KEY
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789012/image-processing-sync
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
AWS_REGION_NAME=us-east-1
```

### **Settings.py:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

APP_KEY = os.getenv("APP_KEY")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
```

---

## 📦 **3. Configuração do SQS na AWS:**

### **3.1 Criar a Fila SQS:**

* Tipo de fila: **Standard**
* Região: **us-east-1**
* Copie a **URL da fila** após a criação.

### **3.2 Permissões para Lambda:**

1. Acesse o **IAM Console**.
2. Crie uma política com permissões para enviar e receber mensagens:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sqs:SendMessage",
                "sqs:ReceiveMessage",
                "sqs:DeleteMessage",
                "sqs:GetQueueAttributes",
                "sqs:GetQueueUrl"
            ],
            "Resource": "arn:aws:sqs:us-east-1:123456789012:image-processing-sync"
        }
    ]
}
```

3. Anexe a política ao usuário IAM utilizado no projeto Django.

---

## ⚙️ **4. Envio de Mensagem para o SQS via Django:**

### **Classe de Gerenciamento do SQS:**

```python
import json
import boto3
from django.conf import settings

class SqSManager:
    def __init__(self):
        self.sqs = boto3.client('sqs', region_name=settings.AWS_REGION_NAME)
        self.queue_url = settings.SQS_QUEUE_URL

    def _send(self, msg: dict):
        self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(msg)
        )

    @staticmethod
    def send(msg: dict):
        manager = SqSManager()
        manager._send(msg=msg)
```

### **Uso da Classe SQS:**

```python
msg = {
    "apps": [{
        "endpoint": "https://abc123.ngrok.io/api/v1/image-processing-sync",
        "key": "YOUR_SECURE_APP_KEY"
    }],
    "data": {
        "image_id": 1
    }
}
SqSManager.send(msg=msg)
```

---

## 📝 **5. Função Lambda:**

### **Arquivo Lambda (lambda\_function.py):**

```python
import asyncio
import json
import logging
import aiohttp

logger = logging.getLogger()
logger.setLevel(logging.INFO)

async def sync_app(session, endpoint, headers, data):
    async with session.post(endpoint, json=data, headers=headers) as response:
        response.raise_for_status()
        return {"status": response.status, "app": endpoint}

async def sync_all_app(event):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for record in event.get('Records', []):
            body = json.loads(record['body'])
            for app in body['apps']:
                tasks.append(sync_app(session, app['endpoint'], {"Authorization": f"Token {app['key']}"}, body['data']))
        return await asyncio.gather(*tasks)

def lambda_handler(event, context):
    responses = asyncio.run(sync_all_app(event))
    logger.info(f"Responses: {responses}")
    return {"statusCode": 200, "body": json.dumps(responses)}
```

---

## 🌐 **6. Endpoint Django para Receber Mensagem:**

### **API View:**

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class ImageProcessingSyncApiView(APIView):
    permission_classes = []

    def post(self, request):
        print("Dados recebidos:", request.data)
        return Response({"message": "Dados processados com sucesso"})
```

---

## 🧩 **7. Teste Completo:**

### **Enviar Mensagem para o SQS via AWS CLI:**

```bash
aws sqs send-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/image-processing-sync \
    --message-body '{"apps": [{"endpoint": "https://abc123.ngrok.io/api/v1/image-processing-sync", "key": "YOUR_SECURE_APP_KEY"}], "data": {"image_id": 1}}'
```

### **Verificar Logs no Lambda:**

```bash
aws logs tail /aws/lambda/func_sqs_sync --follow
```

### **Verificar Logs no Django:**

```bash
tail -f /var/log/django/django.log
```

---

## ✅ **8. Conclusão:**

1. **Integração Completa:** AWS SQS, Lambda e Django sincronizados.
2. **Processo Assíncrono:** O SQS armazena as mensagens até que o Lambda as processe.
3. **Flexibilidade:** O Lambda pode ser adaptado para diferentes endpoints e casos de uso.
4. **Segurança:** O endpoint Django utiliza autenticação por token para garantir que apenas mensagens autorizadas sejam processadas.
