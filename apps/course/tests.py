from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from apps.course.models import Category, Course, Instructor, Tag


class CourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user1", password="pass123") # noqa501

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Programação")
        self.instructor = Instructor.objects.create(user=self.user)
        self.tag1 = Tag.objects.create(name="django")
        self.tag2 = Tag.objects.create(name="rest")

        self.course = Course.objects.create(
            title="Curso de Teste",
            description="Aprenda Teste na prática",
            price=199.90,
            is_active=True,
            is_free=False,
            workload=40,
            start_date=date(2025, 4, 30),
            category=self.category,
            instructor=self.instructor
        )
        self.course.tags.set([self.tag1])

    def test_create_course(self):
        payload = {
            "title": "Curso de Django",
            "description": "Aprenda Django",
            "price": "99.90",
            "is_active": True,
            "is_free": False,
            "workload": 20,
            "start_date": "2025-04-30",
            "category_id": self.category.id,
            "instructor_id": self.instructor.id,
            "tag_ids": [self.tag1.id, self.tag2.id],
        }

        response = self.client.post("/api/v1/courses/", payload, format="json") # noqa501
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.last().title, "Curso de Django")

    def test_update_course(self):
        payload = {
            "title": "Curso Atualizado",
            "description": self.course.description,
            "price": "179.90",
            "is_active": self.course.is_active,
            "is_free": self.course.is_free,
            "workload": self.course.workload,
            "start_date": self.course.start_date.isoformat(),
            "category_id": self.course.category.id,
            "instructor_id": self.course.instructor.id,
            "tag_ids": [self.tag2.id],
        }

        url = f"/api/v1/courses/{self.course.id}/"
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, 200)

        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Curso Atualizado")
        self.assertIn(self.tag2, self.course.tags.all())

    def test_show_course(self):
        url = f"/api/v1/courses/{self.course.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Curso de Teste")

    # def test_list_course(self):

    #     url = "/api/v1/courses/"
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    #     self.assertIn("results", response.data)
    #     self.assertIsInstance(response.data["results"], list)

    #     print("📚 Cursos retornados:", response.data["results"])
