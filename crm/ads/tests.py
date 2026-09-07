from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from services.models import Service

from .models import Ad

User = get_user_model()


class AdModelUnitTest(TestCase):
    def setUp(self):
        cache.clear()
        self.service = Service.objects.create(title="CRM", price=10000)
        self.ad = Ad.objects.create(
            title="Реклама в Telegram", budget=5000, product=self.service
        )

    def test_ad_mandatory_product_relation(self):
        broken_ad = Ad(title="Кампания без продукта", budget=1000, product=None)
        with self.assertRaises(ValidationError):
            broken_ad.full_clean()

    def test_ad_budget_cannot_be_negative(self):
        bad_ad = Ad(title="Минусовой бюджет", budget=-500, product=self.service)
        with self.assertRaises(ValidationError):
            bad_ad.full_clean()

    def test_ad_soft_delete_triggers_cache_invalidation_via_view(self):
        cache.set("crm_ads_statistic_list", ["cached_report_data"])

        User.objects.create_superuser(
            username="admin_cache_killer", password="password123"
        )

        self.client.login(username="admin_cache_killer", password="password123")

        url = reverse("ads:ads-delete", kwargs={"pk": self.ad.id})
        self.client.post(url)

        self.assertIsNone(
            cache.get("crm_ads_statistic_list"),
            "Кэш аналитики НЕ сбросился! Вьюха удаления не вызвала cache.delete().",
        )
