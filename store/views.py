from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from store.util import Util, token_generator
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Service
from store.forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


class HomeView(TemplateView):
    """ Index view """

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discount_services'] = Service.objects.exclude(discount='0')

        return context


class SignUpView(CreateView):
    """ SignUp view """

    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def send_activation_email(self, request, user):
        """ sends email confirmation email """

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        domain = get_current_site(request).domain
        schema = request.is_secure() and "https" or "http"

        link = reverse('user_activation', kwargs={'uidb64': uidb64, 'token': token})
        url = '{}://{}{}'.format(schema, domain, link)

        payload = {
            'receiver': user.email,
            'email_body': {
                'username': user.username,
                'email_body': 'Verify your email to finish signing up for RapidReady',
                'link': url,
                'link_text': 'Verify Your Email',
                'email_reason': "You're receiving this email because you signed up in {}".format(domain),
                'site_name': domain
            },
            'email_subject': 'Verify your Email',
        }

        Util.send_email(payload)
        messages.success(request, 'Please Confirm your email to complete registration.')

    def get(self, request, *args, **kwargs):
        """ Prevents authenticated user accessing registration path """

        if request.user.is_authenticated:
            return redirect('home')
        return super(SignUpView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """ Handles valid form """

        form = self.form_class(self.request.POST)

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.send_activation_email(self.request, user)

        return render(self.request, 'registration/confirm_email.html', {'email': user.email})

    def post(self, request, *args, **kwargs):
        """ Handles existing inactive user registration attempt """

        form = self.form_class(self.request.POST)

        if User.objects.filter(email=request.POST['email']).exists():
            user = User.objects.get(email=request.POST['email'])
            if not user.is_active:
                self.send_activation_email(request, user)

                return render(self.request, 'registration/confirm_email.html', {'email': user.email})
        # if no record found pass to form_valid
        return self.form_valid(form)


class UserActivationView(View):
    """ User activation view """

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            # user does not exists
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, ['Your account activated successfully!'])

            return redirect('home')

        messages.warning(request, ['Invalid confirmation link detected'])
        return redirect('login')
