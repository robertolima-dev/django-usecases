import time

from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task(name='mailer.send_mass_email')
def send_mass_email(subject, content):
    users = User.objects.all()

    for user in users:
        # Simulando envio com um print e um sleep
        print(f"Enviando email para: {user.email}")
        time.sleep(0.5)

    print(f"Finalizado envio para {users.count()} usuários.")


@shared_task(name='mailer.send_admin_emails')
def send_admin_emails(processing_done):
    users = User.objects.filter(
        profile__access_level='admin'
    )

    for user in users:
        # Simulando envio com um print e um sleep
        print(f"Enviando email para o admin: {user.email} do processo: {processing_done}") # noqa501
        time.sleep(0.5)
