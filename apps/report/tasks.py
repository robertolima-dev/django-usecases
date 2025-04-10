import csv
import os

from celery import shared_task
from django.contrib.auth.models import User
from django.utils.timezone import now

from apps.report.models import ReportRequest


@shared_task(name='report.generate_user_report')
def generate_user_report(report_id):
    report = None

    try:
        report = ReportRequest.objects.filter(id=report_id).first()

        if not report:
            return

        report.status = "processing"
        report.save()

        users = User.objects.filter(is_active=True)

        file_name = f"users_report_{report.id}.csv"
        file_dir = os.path.join("media", "reports")
        os.makedirs(file_dir, exist_ok=True)
        file_path = os.path.join(file_dir, file_name)

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Username", "Email", "Data de Criação"])
            for user in users:
                writer.writerow([user.id, user.username, user.email, user.date_joined.strftime("%Y-%m-%d %H:%M:%S")]) # noqa501

        report.status = "done"
        report.file_path = f"/{file_path}"
        report.completed_at = now()
        report.save()

    except Exception as e:
        print(str(e))
        if report:
            report.status = "failed"
            report.completed_at = now()
            report.save()
        raise e
