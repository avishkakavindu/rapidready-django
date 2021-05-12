from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.views.generic.edit import FormMixin, UpdateView
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse, HttpResponse
from rest_framework import permissions, status
from store.permissions import IsOwner
from store.serializers import OrderSerializer, QuoteSerializer, CartItemSerializer
from store.util import Util, token_generator
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Service, Category, Review, Order, OrderedService, Quote, CartItem, Cart
from store.forms import SignUpForm, AddToCartForm, ServiceReviewForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import serializers
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response

User = get_user_model()


class HomeView(generic.TemplateView):
    """ Index view """

    template_name = "store/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discount_services'] = Service.objects.exclude(discount='0')

        return context


class SignUpView(generic.CreateView):
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


class UserActivationView(generic.View):
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


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    """ Profile details view """

    model = User
    template_name = 'registration/profile.html'
    fields = ['first_name', 'last_name', 'email', 'nic', 'street', 'city', 'state', 'zipcode', 'telephone',
              'profile_pic']
    login_url = '/login'
    context_object_name = 'user'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context['orders'] = Order.objects.filter(customer=self.request.user).prefetch_related(
            Prefetch(
                'orderedservice_set',
                OrderedService.objects.all(),
                to_attr='services'
            ),
        )
        context['category_tags'] = OrderedService.objects.only('service__category').distinct();
        return context


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Password changed successfully!')
        return reverse('profile')


class ServiceView(FormMixin, generic.DetailView):
    """ Service detail view """

    model = Service
    template_name = 'store/service.html'
    form_class = ServiceReviewForm
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data()
        context['reviews'] = Review.objects.filter(service=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """ Handles valid form """
        form = self.form_class(self.request.POST)
        review = form.save(commit=False)
        review.user = self.request.user
        review.service = Service.objects.get(pk=self.kwargs['pk'])
        form.save()
        messages.success(self.request, ['Your review added successfully!'])

        return HttpResponseRedirect(self.request.path_info)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:

            return self.form_invalid(form)


class OrderRetriewAPIView(RetrieveAPIView):
    """ Retrieves Order details API view """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class QuoteCreateAPIView(CreateAPIView):
    """ Create Quote API view """

    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class CartItemCreateAPIView(CreateAPIView):
    """ Create Cart item API view """

    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user).latest('created_on')
        if cart is None or not cart.is_active:
            cart = Cart.objects.create(user=request.user)
        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response({'Detail': 'Service added to cart'}, status=status.HTTP_201_CREATED)
        return Response({'Error': 'Unexpected error occured! Please retry'}, status=status.HTTP_400_BAD_REQUEST)
