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


class LeadsViewList(ListView):
    model = Lead
    template_name = 'leads/leads-list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        return Lead.objects.exclude(status__in=["refused", "converted"])


class LeadsCreateView(CreateView):
    model = Lead
    fields = ['first_name', 'last_name', 'phone', 'email']
    template_name = 'leads/leads-create.html'
    success_url = reverse_lazy("leads:leads-list")


class LeadsDetailView(DetailView):
    model = Lead
    template_name = 'leads/leads-detail.html'


class LeadsUpdateView(UpdateView):
    model = Lead
    fields = ['first_name', 'last_name', 'phone', 'email']
    template_name = 'leads/leads-edit.html'

    def get_success_url(self):
        return reverse_lazy("leads:leads-detail", kwargs={"pk": self.object.pk})


class LeadsDeleteView(DeleteView):
    model = Lead
    template_name = 'leads/leads-delete.html'
    success_url = reverse_lazy("leads:leads-list")

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.status = "refused"
        self.object.save()

        return HttpResponseRedirect(success_url)
