from ads.models import Ad
from customers.models import Customer
from django.views.generic import TemplateView
from leads.models import Lead
from services.models import Service


class DashboardIndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["products_count"] = Service.objects.filter(is_active=True).count()
        context["advertisements_count"] = Ad.objects.filter(is_active=True).count()
        context["leads_count"] = (Lead.objects.
                                  exclude(status__in=["refused", "converted"]).
                                  count())
        context["customers_count"] = Customer.objects.filter(is_active=True).count()

        return context
