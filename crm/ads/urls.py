from django.urls import path

from .views import (
    AdsCreateView,
    AdsDeleteView,
    AdsDetailView,
    AdsListView,
    AdsStatisticListView,
    AdsUpdateView,
)

urlpatterns = [
    path('ads/', AdsListView.as_view(), name='ads-list'),
    path('ads/statistic/', AdsStatisticListView.as_view(), name='ads-statistic'),
    path('ads/new/', AdsCreateView.as_view(), name='ads-create'),
    path('ads/<int:pk>/', AdsDetailView.as_view(), name='ads-detail'),
    path('ads/<int:pk>/edit/', AdsUpdateView.as_view(), name='ads-update'),
    path('ads/<int:pk>/delete/', AdsDeleteView.as_view(), name='ads-delete'),
]
