from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from apps.book.models import Book, Comment, Tag


class BookTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass123") # noqa501
        self.tag1 = Tag.objects.create(name="Django")
        self.tag2 = Tag.objects.create(name="API")

        self.book = Book.objects.create(title="Aprendendo Django", author=self.user) # noqa501
        self.book.tags.add(self.tag1, self.tag2)

        self.comment = Comment.objects.create(book=self.book, content="Excelente livro!") # noqa501

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_book_creation(self):
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(self.book.title, "Aprendendo Django")
        self.assertIn(self.tag1, self.book.tags.all())

    def test_comment_creation(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.book, self.book)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="123456") # noqa501
        self.book = Book.objects.create(title="Python 101", author=self.user) # noqa501
        self.comment = Comment.objects.create(book=self.book, content="Excelente leitura!") # noqa501

    def test_comment_creation(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.book, self.book)
        self.assertEqual(self.comment.content, "Excelente leitura!")


class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="teste", password="123456") # noqa501
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(title="REST com Django", author=self.user) # noqa501

    def test_list_books(self):
        response = self.client.get("/api/v1/books/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("REST com Django", str(response.data))

    def test_create_book(self):
        response = self.client.post("/api/v1/books/", {
            "title": "Novo Livro",
            "author_id": self.user.id,
            "tag_ids": [],
        }, format="json")
        self.assertEqual(response.status_code, 201)
