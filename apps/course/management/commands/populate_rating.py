# management/commands/rating_populate.py
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.course.models import Course, CourseRating

User = get_user_model()


class Command(BaseCommand):
    help = "Popula avaliações aleatórias para cursos"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        courses = Course.objects.all()

        created = 0
        for course in courses:
            reviewers = random.sample(list(users), min(5, users.count()))
            for user in reviewers:
                rating, _ = CourseRating.objects.get_or_create(
                    course=course,
                    user=user,
                    defaults={
                        "rating": random.randint(1, 5),
                        "comment": f"Avaliação de {user.username}"
                    }
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"{created} avaliações criadas."))  # noqa: E501
