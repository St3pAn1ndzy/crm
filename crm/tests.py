from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.db import transaction
from django.test import TestCase
from django.urls import reverse

from ads.models import Ad
from contracts.models import Contract
from customers.models import Customer
from leads.models import Lead
from services.models import Service

User = get_user_model()


class CrmBusinessLogicTestCase(TestCase):
    def setUp(self):
        cache.clear()

        self.service = Service.objects.create(
            title="Тестовая услуга", price=10000, is_active=True
        )
        self.ad = Ad.objects.create(
            title="Яндекс.Директ", budget=5000, product=self.service, is_active=True
        )
        self.lead_in_work = Lead.objects.create(
            first_name="Иван",
            last_name="ПростоЛид",
            status="new",
            advertisement=self.ad,
        )
        self.lead_refused = Lead.objects.create(
            first_name="Клиент",
            last_name="Отказной",
            status="refused",
            advertisement=self.ad,
        )
        self.lead_converted = Lead.objects.create(
            first_name="Пётр",
            last_name="Покупатель",
            status="converted",
            advertisement=self.ad,
        )

    def test_user_role_auto_group_assignment(self):
        user = User.objects.create_user(username="test_manager", password="password123")
        user.role = "manager"
        user.save()

        manager_group = Group.objects.get(name="Managers")
        self.assertIn(
            manager_group,
            user.groups.all(),
            "Пользователю не привязалась группа 'Managers'!",
        )

    def test_ads_statistic_sql_logic(self):
        customer = Customer.objects.create(lead=self.lead_converted, is_active=True)

        today = date.today()
        next_year = today + timedelta(days=365)

        Contract.objects.create(
            title="Договор А",
            customer=customer,
            service=self.service,
            cost=30000,
            start_date=today,
            end_date=next_year,
            is_active=True,
        )

        Contract.objects.create(
            title="Договор B",
            customer=customer,
            service=self.service,
            cost=15000,
            start_date=today,
            end_date=next_year,
            is_active=False,
        )

        User.objects.create_superuser(username="admin_tester", password="password")
        self.client.login(username="admin_tester", password="password")

        response = self.client.get(reverse("ads:ads-statistic"))
        self.assertEqual(response.status_code, 200)

        ad_metrics = next(ad for ad in response.context["ads"] if ad.id == self.ad.id)

        self.assertEqual(
            ad_metrics.leads_count,
            2,
            "Неверный подсчет лидов с учетом отсечения отказа!",
        )
        self.assertEqual(
            ad_metrics.customers_count, 1, "Неверный подсчет активных клиентов!"
        )
        self.assertEqual(ad_metrics.profit, 25000, "Ошибка в расчете чистой прибыли!")

    def test_role_based_access_control_security(self):
        operator = User.objects.create_user(
            username="operator_tester", password="password"
        )
        operator.role = "operator"
        operator.save()

        self.client.login(username="operator_tester", password="password")
        response = self.client.get(reverse("ads:ads-statistic"))

        self.assertEqual(
            response.status_code,
            403,
            "Дыра в безопасности! Оператор смог открыть страницу статистики!",
        )

    def test_contract_delete_view_soft_deletes_contract(self):
        customer = Customer.objects.create(lead=self.lead_converted, is_active=True)
        today = date.today()

        contract = Contract.objects.create(
            customer=customer,
            service=self.service,
            cost=5000,
            start_date=today,
            end_date=today + timedelta(days=30),
            is_active=True,
        )

        User.objects.create_superuser(username="delete_manager", password="password")
        self.client.login(username="delete_manager", password="password")

        url = reverse("contracts:contracts-delete", kwargs={"pk": contract.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        db_contract = Contract.objects.get(id=contract.id)

        self.assertFalse(
            db_contract.is_active,
            "View удаления физически стерла контракт или "
            "не переключила флаг is_active!",
        )

    def test_lead_conversion_transaction_fail(self):
        initial_customers_count = Customer.objects.count()

        try:
            with transaction.atomic():
                new_customer = Customer.objects.create(
                    lead=self.lead_in_work, is_active=True
                )
                Contract.objects.create(
                    customer=new_customer,
                    service=self.service,
                    cost=10000,
                    start_date=None,
                    end_date=None,
                )
        except Exception:
            pass

        self.assertEqual(
            Customer.objects.count(),
            initial_customers_count,
            "Транзакция не откатилась! Битый клиент остался в базе данных.",
        )
