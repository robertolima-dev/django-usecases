from django.conf import settings
from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch

from apps.book.models import Book
from apps.search.services.embedding_service import generate_embedding


class Command(BaseCommand):
    help = "Reindexa todos os livros para o índice semantic_books com embeddings gerados" # noqa501

    def handle(self, *args, **kwargs):
        es = Elasticsearch(
            hosts=[settings.ELASTICSEARCH_HOST],
            basic_auth=(settings.ELASTICSEARCH_USERNAME, settings.ELASTICSEARCH_PASSWORD), # noqa501
            verify_certs=True
        )
        books = Book.objects.all()
        count = 0

        for book in books:
            title_vector = generate_embedding(book.title)

            doc = {
                "id": book.id,
                "title": book.title,
                "title_vector": title_vector
            }

            es.index(
                index="semantic_books",
                id=book.id,
                document=doc
            )

            self.stdout.write(self.style.SUCCESS(f"Indexado semanticamente: {book.title}")) # noqa501
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Total de livros indexados semanticamente: {count}")) # noqa501
