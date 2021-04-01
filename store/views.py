from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from store.models import Service
from store.forms import SignUpForm


class HomeView(TemplateView):
    """ Index page """

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discount_services'] = Service.objects.exclude(discount='0')

        return context


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        form.instance = self.request.POST
        return super().form_valid(form)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email