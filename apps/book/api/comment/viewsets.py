from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.book.models import Comment

from .serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete', ]

    def get_queryset(self):
        queryset = Comment.objects.all().order_by("-created_at")

        if self.action in ['list', 'retrieve']:

            book_id = self.request.query_params.get("book_id")
            if not book_id:
                raise ValidationError({'detail': 'Informe o book_id'})

            queryset = queryset.filter(book_id=book_id)

        return queryset
