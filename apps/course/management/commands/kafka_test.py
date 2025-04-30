import time

from django.core.management.base import BaseCommand

from apps.course.models import Course
from apps.kafka_events.producers.course_producer import \
    send_course_created_event


class Command(BaseCommand):
    help = "Envia 15 eventos Kafka simulando criação de cursos para teste da fila" # noqa501

    def handle(self, *args, **kwargs):
        fake_courses = Course.objects.all()[:15]
        if not fake_courses:
            self.stdout.write(self.style.ERROR("❌ Nenhum curso encontrado para simular.")) # noqa501
            return

        for i, course in enumerate(fake_courses):
            send_course_created_event(course)
            self.stdout.write(self.style.SUCCESS(f"✅ Evento {i+1} enviado para o curso: {course.title}")) # noqa501
            time.sleep(0.5)

        self.stdout.write(self.style.SUCCESS("🎯 Fim do envio dos 15 eventos."))
