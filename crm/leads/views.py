import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Lead

logger = logging.getLogger("crm")


class LeadsViewList(PermissionRequiredMixin, ListView):
    model = Lead
    template_name = 'leads/leads-list.html'
    context_object_name = 'leads'
    permission_required = 'leads.view_lead'

    def get_queryset(self):
        return Lead.objects.exclude(status__in=["refused", "converted"])


class LeadsCreateView(PermissionRequiredMixin, CreateView):
    model = Lead
    fields = ['first_name', 'last_name', 'phone', 'email']
    template_name = 'leads/leads-create.html'
    success_url = reverse_lazy("leads:leads-list")
    permission_required = 'leads.add_lead'

    def form_valid(self, form):
        response = super().form_valid(form)

        logger.info(
            f"Пользователь '{self.request.user.username}' добавил нового лида: "
            f"'({self.object.first_name} {self.object.last_name}). "
            f"(ID: {self.object.id})"
        )

        cache.delete("crm_ads_statistic_list")
        logger.info("Кэш статистики рекламы автоматически сброшен из-за добавления нового контракта.")

        return response


class LeadsDetailView(PermissionRequiredMixin, DetailView):
    model = Lead
    template_name = 'leads/leads-detail.html'
    permission_required = 'leads.view_lead'


class LeadsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Lead
    fields = ['first_name', 'last_name', 'phone', 'email']
    template_name = 'leads/leads-edit.html'
    permission_required = 'leads.change_lead'

    def get_success_url(self):
        return reverse_lazy("leads:leads-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)

        logger.info(
            f"Пользователь '{self.request.user.username}' отредактировал данные лида "
            f"'{self.object.first_name} {self.object.last_name}'. "
            f"(ID: {self.object.id})"
        )

        return response


class LeadsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Lead
    template_name = 'leads/leads-delete.html'
    success_url = reverse_lazy("leads:leads-list")
    permission_required = 'leads.delete_lead'

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.status = "refused"
        self.object.save()

        logger.warning(
            f"Пользователь '{self.request.user.username}' присвоил статус ОТКАЗ "
            f"клиенту '{self.object.first_name} {self.object.last_name}' "
            f"(ID: {self.object.id})"
        )

        return HttpResponseRedirect(success_url)
