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


class AdsListView(ListView):
    model = Ad
    template_name = 'ads/ads-list.html'
    context_object_name = 'ads'

    def get_queryset(self):
        return Ad.objects.only('title').filter(is_active=True)


class AdsCreateView(CreateView):
    model = Ad
    fields = ["title", "channel", "product", "budget"]
    template_name = 'ads/ads-create.html'
    success_url = reverse_lazy("ads-list")


class AdsDetailView(DetailView):
    model = Ad
    template_name = 'ads/ads-detail.html'


class AdsUpdateView(UpdateView):
    model = Ad
    fields = ["title", "channel", "product", "budget"]
    template_name = 'ads/ads-edit.html'

    def get_queryset(self):
        return Ad.objects.only("title", "channel", "product", "budget")

    def get_success_url(self):
        return reverse_lazy("ads-detail", kwargs={"pk": self.object.pk})


class AdsDeleteView(DeleteView):
    model = Ad
    template_name = 'ads/ads-delete.html'
    success_url = reverse_lazy("ads-list")

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(success_url)


class AdsStatisticListView(ListView):
    model = Ad
    template_name = 'ads/ads-statistic.html'
    context_object_name = 'ads'

    def get_queryset(self):
        return Ad.objects.all()
