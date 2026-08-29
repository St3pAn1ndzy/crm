from django.urls import path

from .views import (
    ContractsCreateView,
    ContractsDeleteView,
    ContractsDetailView,
    ContractsListView,
    ContractsUpdateView,
)

app_name = "contracts"

urlpatterns = [
    path("contracts/", ContractsListView.as_view(), name="contracts-list"),
    path("contracts/new/", ContractsCreateView.as_view(), name="contracts-create"),
    path("contracts/<int:pk>/", ContractsDetailView.as_view(), name="contracts-detail"),
    path(
        "contracts/<int:pk>/edit/",
        ContractsUpdateView.as_view(),
        name="contracts-update",
    ),
    path(
        "contracts/<int:pk>/delete/",
        ContractsDeleteView.as_view(),
        name="contracts-delete",
    ),
]
