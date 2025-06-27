import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from faker import Faker

from apps.course.models import Category, Course, Instructor, Tag

User = get_user_model()
fake = Faker("pt_BR")


class Command(BaseCommand):
    help = "Popula o app course com 30 cursos, categorias, instrutores e tags"

    def handle(self, *args, **kwargs):
        categories = ["Tecnologia", "Negócios", "Saúde", "Artes", "Linguagens"]
        category_objs = [Category.objects.get_or_create(name=name)[0] for name in categories]  # noqa: E501

        tag_names = ["python", "django", "api", "design", "data", "ux", "sql", "frontend"]  # noqa: E501
        tag_objs = [Tag.objects.get_or_create(name=tag)[0] for tag in tag_names]  # noqa: E501

        instructors = []
        for i in range(5):
            user, _ = User.objects.get_or_create(
                username=f"instrutor{i+1}",
                defaults={"email": f"instrutor{i+1}@curso.com", "password": "123456"},  # noqa: E501
            )
            inst, _ = Instructor.objects.get_or_create(user=user, defaults={"bio": fake.text()})  # noqa: E501
            instructors.append(inst)

        for i in range(50):
            course = Course.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=5),
                price=random.choice([0, 49.90, 99.90, 149.90, 299.90, 399.90]),
                is_free=random.choice([True, False]),
                is_active=random.choice([True, True, False]),
                workload=random.randint(5, 60),
                start_date=now().date() + timedelta(days=random.randint(1, 60)),  # noqa: E501
                category=random.choice(category_objs),
                instructor=random.choice(instructors),
            )
            course.tags.set(random.sample(tag_objs, k=random.randint(1, 4)))
            self.stdout.write(f"✔️ Curso criado: {course.title}")

        self.stdout.write(self.style.SUCCESS("🎉 30 cursos criados com sucesso!"))  # noqa: E501
