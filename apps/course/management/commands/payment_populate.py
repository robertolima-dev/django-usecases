# management/commands/payment_populate.py
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.course.models import Course, CoursePayment

User = get_user_model()


class Command(BaseCommand):
    help = "Popula pagamentos aleatórios para cursos"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        courses = Course.objects.all()
        statuses = ['paid', 'pending', 'failed']
        created = 0

        for course in courses:
            buyers = random.sample(list(users), min(8, users.count()))
            for user in buyers:
                CoursePayment.objects.create(
                    course=course,
                    user=user,
                    status=random.choices(statuses, weights=[0.6, 0.3, 0.1])[0]
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"{created} pagamentos criados."))
