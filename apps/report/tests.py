from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from apps.report.models import ReportRequest
from apps.report.tasks import generate_user_report


class ReportRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass123")  # noqa: E501
        self.report = ReportRequest.objects.create(
            user=self.user,
            status="pending"
        )

    def test_report_creation(self):
        self.assertEqual(ReportRequest.objects.count(), 1)
        self.assertEqual(self.report.status, "pending")
        self.assertEqual(self.report.user, self.user)

    def test_report_status_update(self):
        self.report.status = "processing"
        self.report.save()
        self.assertEqual(self.report.status, "processing")

    def test_report_completion(self):
        self.report.status = "done"
        self.report.save()
        self.assertEqual(self.report.status, "done")


class ReportAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="teste", password="123456")  # noqa: E501
        self.client.force_authenticate(user=self.user)
        self.report = ReportRequest.objects.create(
            user=self.user,
            status="pending"
        )

    def test_list_reports(self):
        response = self.client.get("/api/v1/reports/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(self.report.id), str(response.data))

    def test_create_report(self):
        response = self.client.post("/api/v1/reports/", {}, format="json")
        self.assertEqual(response.status_code, 201)

    @patch('apps.report.tasks.generate_user_report.delay')
    def test_report_processing_flow(self, mock_task):
        # Create a new report
        response = self.client.post("/api/v1/reports/", {}, format="json")
        self.assertEqual(response.status_code, 201)
        report_id = response.data['id']

        # Simulate the task being called
        mock_task.return_value = None
        generate_user_report(report_id)

        # Check the report status
        response = self.client.get(f"/api/v1/reports/{report_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], "done")
