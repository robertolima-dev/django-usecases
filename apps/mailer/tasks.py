import time

# import boto3
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

from apps.mailer.models import EmailLog, EmailTemplate

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
def send_admin_emails(template_name, context):
    users = User.objects.filter(
        profile__access_level='admin'
    )
    print(users)

    if users:
        for user in users:
            print(user)

            context['username'] = user.username

            send_email.delay(user.email, template_name, context)
            print(f"Enviado email para o admin: {user.email} - Processo: {template_name}") # noqa501


@shared_task(name='mailer.send_email')
def send_email(recipient, template_name, context):
    try:
        template = EmailTemplate.objects.get(name=template_name)

        html_content = template.html_content.format(**context)

        email = EmailMessage(
            subject=template.subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )
        email.content_subtype = 'html'

        email.send()

        EmailLog.objects.create(
            recipient=recipient,
            subject=template.subject,
            template=template,
            status='sent',
            response='Email enviado com sucesso.',
            context=context
        )
    except Exception as e:
        EmailLog.objects.create(
            recipient=recipient,
            subject="Erro",
            template=None,
            status='failed',
            response=str(e),
            context=context
        )
