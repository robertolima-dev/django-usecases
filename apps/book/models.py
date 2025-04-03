from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, ) # noqa501
    tags = models.ManyToManyField(Tag, db_index=True, )


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments', db_index=True, ) # noqa501
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
