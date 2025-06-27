import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from apps.book.models import Book, Comment

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Popula a base de dados com comentários nos livros."

    def handle(self, *args, **options):
        books = list(Book.objects.all())
        if not books:
            self.stdout.write(self.style.WARNING("Nenhum livro encontrado. Execute `populate_books` primeiro."))  # noqa: E501
            return

        comments_created = 0
        for _ in range(300):  # 300 comentários no total
            book = random.choice(books)
            user_id = random.randint(1, 50)

            try:
                User.objects.get(id=user_id)
            except User.DoesNotExist:
                continue

            Comment.objects.create(
                book=book,
                content=fake.sentence(nb_words=random.randint(8, 20))
            )
            comments_created += 1

        self.stdout.write(self.style.SUCCESS(f"{comments_created} comentários criados com sucesso."))  # noqa: E501
