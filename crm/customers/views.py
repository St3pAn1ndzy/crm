import logging

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from contracts.models import Contract

from .forms import ConvertLeadForm, CustomerEditForm
from .models import Customer

logger = logging.getLogger("crm")


class CustomersListView(PermissionRequiredMixin, ListView):
    model = Customer
    template_name = 'customers/customers-list.html'
    context_object_name = 'customers'
    permission_required = 'customers.view_customer'

    def get_queryset(self):
        return (
            Customer.objects.filter(is_active=True)
            .select_related('lead')
        )


class CustomerDetailView(PermissionRequiredMixin, DetailView):
    model = Customer
    template_name = 'customers/customers-detail.html'
    permission_required = 'customers.view_customer'


class CustomerUpdateView(PermissionRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerEditForm
    template_name = 'customers/customers-edit.html'
    permission_required = 'customers.change_customer'

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)

        lead = self.object.lead

        lead.first_name = form.cleaned_data["first_name"]
        lead.last_name = form.cleaned_data["last_name"]
        lead.phone = form.cleaned_data["phone"]
        lead.email = form.cleaned_data["email"]
        lead.save()

        logger.info(
            f"Пользователь '{self.request.user.username}' отредактировал "
            f"данные клиента "
            f"'{lead.first_name} {lead.last_name}' (ID: {self.object.id})."
        )

        return response

    def get_success_url(self):
        return reverse_lazy("customers:customers-detail", kwargs={"pk": self.object.pk})


class CustomerDeleteView(PermissionRequiredMixin, DeleteView):
    model = Customer
    template_name = 'customers/customers-delete.html'
    success_url = reverse_lazy("customers:customers-list")
    permission_required = "customers.delete_customer"

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.is_active = False
        self.object.save()

        logger.warning(
            f"Пользователь '{self.request.user.username}' отправил в архив "
            f"клиента '{self.object.first_name} {self.object.last_name}' "
            f"(ID: {self.object.id})"
        )

        return HttpResponseRedirect(success_url)


@permission_required("customers.add_customer", raise_exception=True)
@transaction.atomic
def convert_lead_to_customer_view(request):
    if request.method == 'POST':
        form = ConvertLeadForm(request.POST, request.FILES)
        if form.is_valid():
            lead = form.cleaned_data['lead']
            try:
                customer = Customer.objects.create(
                    lead=lead
                )

                Contract.objects.create(
                    customer=customer,
                    title=form.cleaned_data['contract_title'],
                    service=form.cleaned_data['service'],
                    document=form.cleaned_data['document'],
                    start_date=form.cleaned_data['start_date'],
                    end_date=form.cleaned_data['end_date'],
                    cost=form.cleaned_data['cost']
                )

                lead.status = "converted"
                lead.save()

                cache.delete("crm_ads_statistic_list")
                logger.info("Кэш статистики рекламы автоматически "
                            "сброшен из-за конвертации лида.")

                logger.info(
                    f"Пользователь {request.user.username} успешно "
                    f"перевел лида #{lead.id} "
                    f"({lead.first_name} {lead.last_name}) в статус Активного клиента."
                )

                return redirect('customers:customers-list')

            except Exception as e:
                logger.error(
                    f"Ошибка при попытке конвертации лида #{lead.id} "
                    f"пользователем {request.user.username}: {str(e)}"
                )
                raise e
    else:
        form = ConvertLeadForm()

    return render(request, "customers/customers-create.html", {"form": form})
