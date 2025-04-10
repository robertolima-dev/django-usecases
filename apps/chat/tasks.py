import time

from celery import shared_task

from apps.mailer.tasks import send_admin_emails


@shared_task(name='chat.process_room')
def process_room(room_id):
    print(f"🔄 Processando sala {room_id}...")
    time.sleep(5)
    print(f"✅ Sala {room_id} processada.")

    send_admin_emails.delay(processing_done=f"room_id:{room_id}")
