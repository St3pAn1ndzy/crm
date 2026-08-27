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

from .models import Lead


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


class LeadsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Lead
    template_name = 'leads/leads-delete.html'
    success_url = reverse_lazy("leads:leads-list")
    permission_required = 'leads.delete_lead'

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.status = "refused"
        self.object.save()

        return HttpResponseRedirect(success_url)
