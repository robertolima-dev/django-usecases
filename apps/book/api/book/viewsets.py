# views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.book.models import Book

from .serializers import BookSerializer


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'put', 'delete', ]

    def get_queryset(self):
        return (
            Book.objects
                .select_related("author")
                .prefetch_related("tags", "comments")
            )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
