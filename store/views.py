from django.views.generic import TemplateView
from store.models import Service


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discount_services'] = Service.objects.exclude(discount='0')

        return context
