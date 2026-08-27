from django.urls import path

from .views import (
    LeadsCreateView,
    LeadsDeleteView,
    LeadsDetailView,
    LeadsUpdateView,
    LeadsViewList,
)

urlpatterns = [
    path('leads/', LeadsViewList.as_view(), name='leads-list'),
    path('leads/new/', LeadsCreateView.as_view(), name='leads-create'),
    path('leads/<int:pk>/', LeadsDetailView.as_view(), name='leads-detail'),
    path('leads/<int:pk>/edit/', LeadsUpdateView.as_view(), name='leads-update'),
    path('leads/<int:pk>/delete/', LeadsDeleteView.as_view(), name='leads-delete'),
]
