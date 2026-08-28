from django.contrib.auth.mixins import PermissionRequiredMixin
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


class ContractsListView(PermissionRequiredMixin, ListView):
    model = Contract
    template_name = 'contracts/contracts-list.html'
    context_object_name = 'contracts'
    permission_required = 'contracts.view_contract'

    def get_queryset(self):
        return (
            Contract.objects.filter(is_active=True)
            .select_related('customer__lead', 'service')
        )


class ContractsDetailView(PermissionRequiredMixin, DetailView):
    model = Contract
    template_name = 'contracts/contracts-detail.html'
    permission_required = 'contracts.view_contract'


class ContractsCreateView(PermissionRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contracts-create.html'
    success_url = reverse_lazy('contracts:contracts-list')
    permission_required = "contracts.add_contract"


class ContractsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contracts-edit.html'
    permission_required = 'contracts.change_contract'


class ContractsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Contract
    template_name = 'contracts/contracts-delete.html'
    success_url = reverse_lazy('contracts:contracts-list')
    permission_required = 'contracts.delete_contract'

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(success_url)
