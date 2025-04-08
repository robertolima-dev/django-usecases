import time

from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_mass_email(subject, content):
    users = User.objects.all()

    for user in users:
        # Simulando envio com um print e um sleep
        print(f"Enviando email para: {user.email}")
        time.sleep(0.5)

    print(f"Finalizado envio para {users.count()} usuários.")
