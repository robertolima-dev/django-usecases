import json

import boto3
from django.conf import settings


class SqSManager:

    def __init__(self) -> None:
        self.sqs = boto3.client('sqs', region_name='us-east-1')
        self.queue_url = settings.SQS_QUEUE_URL

    def _send(self, msg: dict) -> None:
        self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=(json.dumps(msg))
        )

    @staticmethod
    def send(msg: dict) -> None:
        manager = SqSManager()
        manager._send(msg=msg)
