import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from apps.book.models import Book, Tag

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Popula a base de dados com livros de teste."

    def handle(self, *args, **options):
        tags = list(Tag.objects.all())
        if not tags:
            self.stdout.write(self.style.WARNING("Nenhuma tag encontrada. Criando algumas..."))  # noqa: E501
            tags = [Tag.objects.create(name=name) for name in ["Ação", "Drama", "Terror", "Fantasia", "Suspense"]]  # noqa: E501

        books_created = 0
        for _ in range(100):
            author_id = random.randint(1, 50)
            try:
                author = User.objects.get(id=author_id)
            except User.DoesNotExist:
                continue

            book = Book.objects.create(
                title=fake.sentence(nb_words=3),
                author=author
            )
            book.tags.set(random.sample(tags, k=random.randint(1, 3)))
            books_created += 1

        self.stdout.write(self.style.SUCCESS(f"{books_created} livros criados com sucesso."))  # noqa: E501
