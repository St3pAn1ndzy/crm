import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.db.models.aggregates import Count, Sum
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Ad

logger = logging.getLogger("crm")


class AdsListView(PermissionRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/ads-list.html'
    context_object_name = 'ads'
    permission_required = "ads.view_ad"

    def get_queryset(self):
        return (
            Ad.objects.filter(is_active=True)
            .select_related('product')
        )


class AdsCreateView(PermissionRequiredMixin, CreateView):
    model = Ad
    fields = ["title", "channel", "product", "budget"]
    template_name = 'ads/ads-create.html'
    success_url = reverse_lazy("ads:ads-list")
    permission_required = "ads.add_ad"

    def form_valid(self, form):
        response = super().form_valid(form)

        logger.info(
            f"Пользователь '{self.request.user.username}' добавил новую "
            f"рекламную кампанию: "
            f"'{self.object.title}' с бюджетом {self.object.budget} руб. "
            f"(ID: {self.object.id})"
        )

        return response


class AdsDetailView(PermissionRequiredMixin, DetailView):
    model = Ad
    template_name = 'ads/ads-detail.html'
    permission_required = "ads.view_ad"


class AdsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Ad
    fields = ["title", "channel", "product", "budget"]
    template_name = 'ads/ads-edit.html'
    permission_required = "ads.change_ad"

    def get_success_url(self):
        return reverse_lazy("ads:ads-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)

        logger.info(
            f"Пользователь '{self.request.user.username}' обновил рекламную кампанию: "
            f"'{self.object.title}' с бюджетом {self.object.budget} руб. "
            f"(ID: {self.object.id})"
        )

        return response


class AdsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ads/ads-delete.html'
    success_url = reverse_lazy("ads:ads-list")
    permission_required = "ads.delete_ad"

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.is_active = False
        self.object.save()

        logger.warning(
            f"Пользователь '{self.request.user.username}' отправил в архив "
            f"рекламную кампанию '{self.object.title}' (ID: {self.object.id})"
        )

        return HttpResponseRedirect(success_url)


class AdsStatisticListView(PermissionRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/ads-statistic.html'
    context_object_name = 'ads'
    permission_required = "ads.view_ad"

    def get_queryset(self):
        cache_key = "crm_ads_statistic_list"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            logger.info("Статистика рекламы успешно загружена ИЗ КЭША (без запросов к БД).")
            return cached_data

        logger.warning("Кэш пуст! Запускается тяжелый расчет статистики по базе данных PostgreSQL...")

        campaigns = Ad.objects.annotate(
            leads_count=Count('lead', distinct=True),
            customers_count=Count('lead__customer', distinct=True),
            profit=Sum('lead__customer__contract__cost'))

        cached_list = list(campaigns)
        cache.set(cache_key, cached_list, 86400)

        return cached_list
