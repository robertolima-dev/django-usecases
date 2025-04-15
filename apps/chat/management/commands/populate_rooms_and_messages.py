
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from apps.chat.models import Message, Room

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Popula o sistema com Rooms e Mensagens aleatórias."

    def handle(self, *args, **options):
        users = list(User.objects.all())
        if len(users) < 2:
            self.stdout.write(self.style.ERROR("É necessário pelo menos 2 usuários.")) # noqa501
            return

        num_rooms = 10
        num_messages_per_room = 10
        created_rooms = []

        for _ in range(num_rooms):
            participants = random.sample(users, k=random.randint(2, 4))
            room = Room.objects.create(owner=participants[0])
            room.users.set(participants)
            created_rooms.append(room)

        self.stdout.write(self.style.SUCCESS(f"{len(created_rooms)} salas criadas.")) # noqa501

        for room in created_rooms:
            participants = list(room.users.all())
            for _ in range(num_messages_per_room):
                sender = random.choice(participants)
                content = {
                    "text": fake.sentence(nb_words=10),
                }
                Message.objects.create(
                    room=room,
                    sender=sender,
                    type_message="text",
                    content=content,
                    timestamp=timezone.now()
                )

        self.stdout.write(self.style.SUCCESS(f"{num_rooms * num_messages_per_room} mensagens geradas.")) # noqa501
