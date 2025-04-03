import requests
from django.core.management.base import BaseCommand

REGISTER_URL = "http://localhost:8000/api/v1/register-user/"  # Se usar JWT


class Command(BaseCommand):
    help = "Cadastra 50 usuarios"

    def handle(self, *args, **kwargs):

        for i in list(range(1, 50)):
            requests.post(REGISTER_URL, data={"email": "robertolima.izphera+user" + str(i) + "@gmail.com", "password": "123456", "name": "Roberto Lima"}) # noqa501
