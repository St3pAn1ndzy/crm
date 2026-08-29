from django.urls import path

from services.views import (
    ServicesCreateView,
    ServicesDeleteView,
    ServicesDetailView,
    ServicesListView,
    ServicesUpdateView,
)

app_name = "services"

urlpatterns = [
    path("products/", ServicesListView.as_view(), name="products-list"),
    path("products/new/", ServicesCreateView.as_view(), name="products-create"),
    path("products/<int:pk>/", ServicesDetailView.as_view(), name="products-detail"),
    path(
        "products/<int:pk>/edit/", ServicesUpdateView.as_view(), name="products-update"
    ),
    path(
        "products/<int:pk>/delete/",
        ServicesDeleteView.as_view(),
        name="products-delete",
    ),
]
