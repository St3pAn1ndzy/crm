from contracts.models import Contract
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

from .forms import ConvertLeadForm, CustomerEditForm
from .models import Customer


class CustomersListView(ListView):
    model = Customer
    template_name = 'customers/customers-list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.filter(is_active=True)


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customers-detail.html'


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerEditForm
    template_name = 'customers/customers-edit.html'

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)

        lead = self.object.lead

        lead.first_name = form.cleaned_data["first_name"]
        lead.last_name = form.cleaned_data["last_name"]
        lead.phone = form.cleaned_data["phone"]
        lead.email = form.cleaned_data["email"]
        lead.save()

        return response

    def get_success_url(self):
        return reverse_lazy("customers:customers-detail", kwargs={"pk": self.object.pk})


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/customers-delete.html'
    success_url = reverse_lazy("customers:customers-list")

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(success_url)


@transaction.atomic
def convert_lead_to_customer_view(request):
    if request.method == 'POST':
        form = ConvertLeadForm(request.POST, request.FILES)
        if form.is_valid():
            lead = form.cleaned_data['lead']

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

            return redirect('customers:customers-list')
    else:
        form = ConvertLeadForm()

    return render(request, "customers/customers-create.html", {"form": form})
