
import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Simula 51 requisições autenticadas para testar o throttle do plano 'free'"  # noqa: E501

    def add_arguments(self, parser):
        parser.add_argument('--token', type=str, help='Token JWT de autenticação')  # noqa: E501

    def handle(self, *args, **options):
        token = options['token']
        if not token:
            self.stdout.write(self.style.ERROR("Você deve informar um token JWT com --token"))  # noqa: E501
            return

        url = "http://localhost:8000/api/v1/books/"
        headers = {"Authorization": f"Token {token}"}

        for i in range(51):
            response = requests.get(url, headers=headers)
            status = response.status_code
            print(f"{i+1:02d} - HTTP {status} - {response.reason}")
