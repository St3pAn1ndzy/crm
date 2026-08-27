from django.contrib.auth.mixins import PermissionRequiredMixin
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


class AdsListView(PermissionRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/ads-list.html'
    context_object_name = 'ads'
    permission_required = "ads.view_ad"

    def get_queryset(self):
        return Ad.objects.filter(is_active=True)


class AdsCreateView(PermissionRequiredMixin, CreateView):
    model = Ad
    fields = ["title", "channel", "product", "budget"]
    template_name = 'ads/ads-create.html'
    success_url = reverse_lazy("ads-list")
    permission_required = "ads.add_ad"


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
        return reverse_lazy("ads-detail", kwargs={"pk": self.object.pk})


class AdsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ads/ads-delete.html'
    success_url = reverse_lazy("ads-list")
    permission_required = "ads.delete_ad"

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(success_url)


class AdsStatisticListView(PermissionRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/ads-statistic.html'
    context_object_name = 'ads'
    permission_required = "ads.view_ad"

    def get_queryset(self):
        return Ad.objects.annotate(
            leads_count=Count('lead', distinct=True),
            customers_count=Count('lead__customer', distinct=True),
            profit=Sum('lead__customer__contract__cost'))
