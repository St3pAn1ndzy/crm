import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ContractForm
from .models import Contract

logger = logging.getLogger("crm")


class ContractsListView(PermissionRequiredMixin, ListView):
    model = Contract
    template_name = "contracts/contracts-list.html"
    context_object_name = "contracts"
    permission_required = "contracts.view_contract"

    def get_queryset(self):
        return Contract.objects.filter(is_active=True).select_related(
            "customer__lead", "service"
        )


class ContractsDetailView(PermissionRequiredMixin, DetailView):
    model = Contract
    template_name = "contracts/contracts-detail.html"
    permission_required = "contracts.view_contract"


class ContractsCreateView(PermissionRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-create.html"
    success_url = reverse_lazy("contracts:contracts-list")
    permission_required = "contracts.add_contract"

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)

        logger.info(
            f"Пользователь '{self.request.user.username}' добавил новый контракт: "
            f"'{self.object.title}' со сроком до {self.object.end_date}. "
            f"(ID: {self.object.id})"
        )

        cache.delete("crm_ads_statistic_list")
        logger.info(
            "Кэш статистики рекламы автоматически сброшен из-за "
            "добавления нового контракта."
        )

        return response


class ContractsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-edit.html"
    permission_required = "contracts.change_contract"
    success_url = reverse_lazy("contracts:contracts-list")

    def form_valid(self, form):
        response = super().form_valid(form)

        logger.info(
            f"Пользователь '{self.request.user.username}' обновил контракт: "
            f"'{self.object.title}' со сроком до {self.object.end_date}. "
            f"(ID: {self.object.id})"
        )

        cache.delete("crm_ads_statistic_list")
        logger.info(
            "Кэш статистики рекламы автоматически сброшен из-за обновления контракта."
        )

        return response


class ContractsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Contract
    template_name = "contracts/contracts-delete.html"
    success_url = reverse_lazy("contracts:contracts-list")
    permission_required = "contracts.delete_contract"

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.is_active = False
        self.object.save()

        logger.warning(
            f"Пользователь '{self.request.user.username}' отправил в архив "
            f"контракт '{self.object.title}' (ID: {self.object.id})"
        )

        cache.delete("crm_ads_statistic_list")
        logger.info(
            "Кэш статистики рекламы автоматически сброшен из-за расторжения контракта."
        )

        return HttpResponseRedirect(success_url)
