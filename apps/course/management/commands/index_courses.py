from django.core.management.base import BaseCommand

from apps.course.documents import CourseDocument
from apps.course.models import Course


class Command(BaseCommand):
    help = "Indexa todos os cursos existentes no Elasticsearch"

    def handle(self, *args, **kwargs):
        courses = Course.objects.all()
        count = 0

        for course in courses:
            CourseDocument.update_or_create_document(course)
            self.stdout.write(self.style.SUCCESS(f"Indexado: {course.title}"))
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Total de produtos indexados: {count}")) # noqa501
