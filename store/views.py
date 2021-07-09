from decimal import Decimal
from django.db.models import Q
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
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from rest_framework import permissions, status
from rest_framework.views import APIView

from store.permissions import IsOwner
from store.serializers import OrderSerializer, QuoteSerializer, CartItemSerializer, CartSerializer, ServiceSerializer
from store.util import Util, token_generator
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Service, Category, Review, Order, OrderedService, Quote, CartItem, Cart
from store.forms import SignUpForm, ServiceReviewForm, DeliveryForm, OrderReviewForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import serializers
from rest_framework.generics import RetrieveAPIView, CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework import filters

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
        # get distinct service categories
        context['category_tags'] = Category.objects.distinct().filter(
            service__in=Service.objects.filter(
                service_set__in=OrderedService.objects.filter(
                    order__in=Order.objects.filter(customer=self.request.user)
                )
            )
        )
        context['review_form'] = OrderReviewForm

        return context

    def post(self, request, *arga, **kwargs):
        self.object = self.get_object()
        print('\n\n\n', request.POST)
        if 'review_form' in request.POST:
            try:
                order = Order.objects.get(Q(review__isnull=True) | Q(review__exact=''), id=request.POST['id'])
            except Order.DoesNotExist:
                messages.error(self.request, 'Failed to save your review. Please retry!')
                return redirect(self.success_url)

            order.review = request.POST['review']
            order.rating = request.POST['rating']
            order.save()
            messages.success(self.request, 'Review saved successfully!')
        else:
            form_class = self.get_form_class()
            form_name = 'form'
            form = self.get_form(form_class)

            if form.is_valid():
                messages.success(self.request, 'Profile info changed!')
                return self.form_valid(form)
            return self.form_invalid(**{form_name: form})
        return redirect(self.success_url)


class PasswordsChangeView(PasswordChangeView):
    """ Password reset view """
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
        messages.success(self.request, 'Your review added successfully!')

        return HttpResponseRedirect(self.request.path_info)

    def form_invalid(self, form):
        """ handles invalid form """
        messages.error(self.request, 'Error occurred while submitting your review!')

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


class CartView(LoginRequiredMixin, generic.TemplateView):
    """ Cart view """

    template_name = 'store/cart.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart.objects.filter(user=self.request.user, is_active=True).prefetch_related(
            Prefetch(
                'cartitem_set',
                CartItem.objects.all(),
                to_attr='cartitems'
            ),
        )
        return context


class CheckoutView(LoginRequiredMixin, FormMixin, generic.TemplateView):
    """ Checkout view  """
    form_class = DeliveryForm
    template_name = 'store/checkout.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Cart.objects.filter(user=self.request.user, is_active=True)
        if not queryset.exists():
            raise Http404
        context['cart'] = queryset
        context['delivery_form'] = self.get_form()
        return context

    def form_valid(self, form):
        """ Handles valid form """
        form = self.form_class(self.request.POST)
        order = form.save(commit=False)          # create a order
        order.customer = self.request.user
        order.type = Order.PREDEFINED
        order.save()

        cart = Cart.objects.filter(user=self.request.user, is_active=True).latest('created_on')
        cart.is_active = False
        cart.save()  # deactivate cart

        for item in cart.cartitem_set.all():
            order_item = OrderedService.objects.create(order=order, service=item.service, quantity=item.quantity, discount=item.service.discount, unit_price=item.service.price)
        messages.success(self.request, 'Your order is processing now.')
        return redirect('profile')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class QuoteCheckoutView(LoginRequiredMixin, generic.View):
    """ Checkout for quote order """
    form_class = DeliveryForm
    template_name = 'store/checkout.html'
    model = Order
    login_url = '/login'

    def get(self, request, quote):
        if not Quote.objects.filter(pk=quote, customer=request.user, order__isnull=True).exists():
            raise Http404

        context = {
            'delivery_form': self.form_class,
            'quote': Quote.objects.get(pk=quote, customer=request.user),
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """ add order type and add relationship to quote """

        quote = Quote.objects.get(pk=self.kwargs['quote'])
        form = DeliveryForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.type = self.model.CUSTOM
            order.desc = quote.order_desc
            order.customer = request.user
            order.save()
            quote.order = order
            quote.save()

            messages.success(self.request, 'Your order is processing now.')
            return redirect('profile')
        messages.error(self.request, 'Error occurred during order processing!')

        context = {
            'delivery_form': form,
            'quote': quote
        }
        print(context)
        return render(request, self.template_name, context)


class QuoteDeleteView(generic.View):
    """ Delete quote view """

    model = Quote
    success_url = 'home'

    def get(self, request, uidb64, token, quote_id, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            try:
                quote = Quote.objects.get(customer=user, pk=quote_id)
            except Quote.DoesNotExist:
                messages.error(request, 'Failed to delete quote!')
                return redirect('home')

            quote.delete()
            messages.success(request, 'Quote deleted successfully!')
            return redirect('home')


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


class CartItemAPIView(CreateModelMixin, GenericAPIView):
    """ Create Cart item API view """

    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user).latest('created_on')
        if cart is None or not cart.is_active:
            item_count = 0
        else:
            item_count = cart.cartitem_set.all().count()
        return Response({'Item Count': item_count}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user).latest('created_on')
        if cart is None or not cart.is_active:
            cart = Cart.objects.create(user=request.user)

        try:
            item = cart.cartitem_set.get(service=request.data['service'])
            cartitem_obj = CartItem.objects.get(id=item.id)
            quantity = Decimal(request.data['quantity']) + item.quantity

            serializer = CartItemSerializer(cartitem_obj, data=request.data)

        except:
            serializer = CartItemSerializer(data=request.data)
            quantity = request.data['quantity']

        if serializer.is_valid():
            serializer.save(cart=cart, quantity=quantity)
            item_count = cart.cartitem_set.all().count()
            return Response({'Detail': 'Service added to cart', 'Item Count': item_count}, status=status.HTTP_201_CREATED)
        return Response({'Error': 'Unexpected error occurred! Please retry'}, status=status.HTTP_400_BAD_REQUEST)


class CartItemDestroyAPIView(APIView):
    """ Destroy Cart item API view """

    def get_object(self, pk):
        try:
            cart = Cart.objects.filter(is_active=True, user=self.request.user).latest('created_on')
            return CartItem.objects.get(pk=pk, cart=cart)
        except:
            raise Http404

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response({'total': item.cart.get_cart_total}, status=status.HTTP_200_OK)


class CartAPIView(RetrieveUpdateDestroyAPIView):
    """ Cart API view  """

    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_object(self):
        try:
            cart = self.queryset.filter(is_active=True, user=self.request.user).latest('created_on')
        except:
            cart = Cart.objects.create(user=self.request.user)

        return cart


class ServiceListAPIView(ListAPIView):
    """ Service API View """

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['service', 'desc', 'category__category']
