from django.core.exceptions import ValidationError
from django.test import TestCase

from ads.models import Ad
from services.models import Service

from .models import Lead


class LeadModelUnitTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(title="Аудит", price=5000)
        self.ad = Ad.objects.create(title="Контекст", budget=1000, product=self.service)
        self.lead = Lead.objects.create(
            first_name="Игорь", last_name="Семенов", status="new", advertisement=self.ad
        )

    def test_lead_default_status(self):
        lead_auto = Lead.objects.create(
            first_name="Анна", last_name="Лид", advertisement=self.ad
        )
        self.assertEqual(lead_auto.status, "new")

    def test_lead_string_format(self):
        self.assertEqual(str(self.lead), "Игорь Семенов (Новый)")

    def test_lead_invalid_status_choices(self):
        invalid_lead = Lead(
            first_name="Тест",
            last_name="Сбой",
            status="broken_status",
            advertisement=self.ad,
        )
        with self.assertRaises(ValidationError):
            invalid_lead.full_clean()
