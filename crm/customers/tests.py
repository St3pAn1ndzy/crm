from django.db import IntegrityError
from django.test import TestCase

from ads.models import Ad
from leads.models import Lead
from services.models import Service

from .models import Customer


class CustomerModelUnitTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(title="Аудит", price=5000)
        self.ad = Ad.objects.create(title="Контекст", budget=1000, product=self.service)
        self.lead = Lead.objects.create(
            first_name="Мария",
            last_name="Кюри",
            status="converted",
            advertisement=self.ad,
        )
        self.customer = Customer.objects.create(lead=self.lead, is_active=True)

    def test_customer_one_to_one_lead_integrity(self):
        self.assertEqual(self.customer.lead, self.lead)

    def test_customer_string_representation(self):
        self.assertEqual(str(self.customer), "Клиент: Мария Кюри")

    def test_customer_duplicate_lead_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Customer.objects.create(lead=self.lead, is_active=True)
