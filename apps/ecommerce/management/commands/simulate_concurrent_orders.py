import random
import threading

import requests
# from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

API_URL = "http://localhost:8000/api/v1/orders/"
LOGIN_URL = "http://localhost:8000/api/v1/auth-user/"  # Se usar JWT


class Command(BaseCommand):
    help = "Simula dois pedidos concorrentes com dois usuários diferentes"

    def handle(self, *args, **kwargs):

        token1 = self.get_token("robertolima.izphera+user1@gmail.com", "123456") # noqa501
        token2 = self.get_token("robertolima.izphera+user2@gmail.com", "123456") # noqa501
        token3 = self.get_token("robertolima.izphera+user3@gmail.com", "123456") # noqa501
        token4 = self.get_token("robertolima.izphera+user4@gmail.com", "123456") # noqa501

        def fazer_pedido(token, nome_usuario):
            response = requests.post(
                API_URL,
                headers={"Authorization": f"Token {token}"},
                json={"product_id": 1, "quantity": random.randint(3, 7)}, # noqa501
            )
            print(f"{nome_usuario} -> {response.status_code} | {response.json()}") # noqa501

        # Dispara os pedidos em paralelo
        t1 = threading.Thread(target=fazer_pedido, args=(token1, "robertolima.izphera+user1@gmail.com")) # noqa501
        t2 = threading.Thread(target=fazer_pedido, args=(token2, "robertolima.izphera+user2@gmail.com")) # noqa501
        t3 = threading.Thread(target=fazer_pedido, args=(token3, "robertolima.izphera+user3@gmail.com")) # noqa501
        t4 = threading.Thread(target=fazer_pedido, args=(token4, "robertolima.izphera+user4@gmail.com")) # noqa501

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

    def get_token(self, username, password):
        response = requests.post(LOGIN_URL, data={"email": username, "password": password}) # noqa501
        if response.status_code == 200:
            return response.json().get("access") or response.json().get("token")  # JWT ou TokenAuth # noqa501
        else:
            raise Exception(f"Erro ao obter token para {username}: {response.content}") # noqa501
