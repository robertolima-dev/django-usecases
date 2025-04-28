from django.contrib.auth.models import User
from django.db import models

from api_core.models import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=50, db_index=True)


class Book(BaseModel):
    title = models.CharField(max_length=100, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books', db_index=True, ) # noqa501
    tags = models.ManyToManyField(Tag, db_index=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["title", "author"]),
        ]

    def __str__(self):
        return self.title  # Book


class Comment(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments', db_index=True, ) # noqa501
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
