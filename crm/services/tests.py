from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Service


class ServiceModelUnitTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(title="Консалтинг", price=15000)

    def test_service_string_representation(self):
        self.assertEqual(str(self.service), "Консалтинг (15000 руб.)")

    def test_service_default_active_status(self):
        self.assertTrue(
            self.service.is_active, "Поле is_active по умолчанию должно быть True"
        )

    def test_service_negative_price_validation(self):
        invalid_service = Service(title="Бесплатный сыр", price=-100)
        with self.assertRaises(ValidationError):
            invalid_service.full_clean()
