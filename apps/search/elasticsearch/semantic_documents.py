from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from apps.book.models import Book

# semantic_index = Index('semantic_books')


@registry.register_document
class SemanticBookDocument(Document):

    class Index:
        name = "semantic_books"

    class Django:
        model = Book
        fields = ["id", "title"]
