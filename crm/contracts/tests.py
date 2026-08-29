from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from ads.models import Ad
from customers.models import Customer
from leads.models import Lead
from services.models import Service

from .models import Contract


class ContractModelUnitTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(title="Курсы", price=20000)
        self.ad = Ad.objects.create(title="FB", budget=5000, product=self.service)
        self.lead = Lead.objects.create(
            first_name="Павел",
            last_name="Дуров",
            status="converted",
            advertisement=self.ad,
        )
        self.customer = Customer.objects.create(lead=self.lead)
        self.contract = Contract.objects.create(
            title="Основной договор",
            customer=self.customer,
            service=self.service,
            cost=30000,
            start_date=date.today(),
            end_date=date.today(),
            is_active=True,
        )

    def test_contract_string_output(self):
        expected_str = f"Договор: Основной договор (от {date.today()})"
        self.assertEqual(str(self.contract), expected_str)

    def test_contract_negative_cost_fails(self):
        bad_contract = Contract(
            title="Сбойный договор",
            customer=self.customer,
            service=self.service,
            cost=-5000,
            start_date=date.today(),
            end_date=date.today(),
        )
        with self.assertRaises(ValidationError):
            bad_contract.full_clean()

    def test_contract_requires_customer(self):
        lost_contract = Contract(
            customer=None,
            service=self.service,
            cost=10000,
            start_date=date.today(),
            end_date=date.today(),
        )
        with self.assertRaises(ValidationError):
            lost_contract.full_clean()

    def test_contract_requires_service(self):
        empty_contract = Contract(
            customer=self.customer,
            service=None,
            cost=10000,
            start_date=date.today(),
            end_date=date.today(),
        )
        with self.assertRaises(ValidationError):
            empty_contract.full_clean()
