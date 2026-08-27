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


class ContractsListView(ListView):
    model = Contract
    template_name = 'contracts/contracts-list.html'
    context_object_name = 'contracts'

    def get_queryset(self):
        return Contract.objects.filter(is_active=True)


class ContractsDetailView(DetailView):
    model = Contract
    template_name = 'contracts/contracts-detail.html'


class ContractsCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contracts-create.html'
    success_url = reverse_lazy('contracts:contracts-list')


class ContractsUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contracts-edit.html'


class ContractsDeleteView(DeleteView):
    model = Contract
    template_name = 'contracts/contracts-delete.html'
    success_url = reverse_lazy('contracts:contracts-list')

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(success_url)
