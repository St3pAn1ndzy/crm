import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
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

from .models import Service

logger = logging.getLogger("crm")


class ServicesListView(PermissionRequiredMixin, ListView):
    model = Service
    template_name = "services/products-list.html"
    context_object_name = "products"
    permission_required = 'services.view_service'

    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class ServicesCreateView(PermissionRequiredMixin, CreateView):
    model = Service
    fields = ["title", "description", "price"]
    template_name = "services/products-create.html"
    success_url = reverse_lazy("services:products-list")
    permission_required = 'services.add_service'

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)

        logger.info(
            f"Пользователь '{self.request.user.username}' добавил новую услугу: "
            f"'{self.object.title}' стоимостью {self.object.price} руб. "
            f"(ID: {self.object.id})"
        )

        return response


class ServicesDetailView(PermissionRequiredMixin, DetailView):
    model = Service
    template_name = "services/products-detail.html"
    permission_required = 'services.view_service'


class ServicesUpdateView(PermissionRequiredMixin, UpdateView):
    model = Service
    fields = ["title", "description", "price"]
    template_name = "services/products-edit.html"
    permission_required = 'services.change_service'

    def get_success_url(self):
        return reverse_lazy("services:products-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)

        logger.info(
            f"Пользователь '{self.request.user.username}' отредактировал услугу "
            f"'{self.object.title}'. (ID: {self.object.id})"
        )

        return response


class ServicesDeleteView(PermissionRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy("services:products-list")
    template_name = "services/products-delete.html"
    permission_required = 'services.delete_service'

    def form_valid(self, form):
        success_url = self.get_success_url()

        self.object.is_active = False
        self.object.save()

        logger.warning(
            f"Пользователь '{self.request.user.username}' отправил в архив "
            f"услугу '{self.object.title}' (ID: {self.object.id})"
        )

        return HttpResponseRedirect(success_url)
