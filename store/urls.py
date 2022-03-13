from django.contrib.auth import views as auth_views
from django.urls import path

from store.views import *

urlpatterns = [
    # auth
    path('', HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>', UserActivationView.as_view(), name='user_activation'),
    # -------------------
    # profile
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-password/', PasswordsChangeView.as_view(), name='change-password'),
    # password reset process
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',
                                             html_email_template_name='registration/password_reset_email.html',
                                             email_template_name='registration/password_reset_email.html',
                                             ),
        name='password_reset'
    ),  # allows a user to reset their password by generating a one-time use link
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),  # after password reset email sent
    path(
        'password_reset_confirm/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),  # present a form to enter new password
    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'
    ),  # inform success
    # ---------------------
    # services
    path('service/<int:pk>/', ServiceView.as_view(), name='service'),
    path('search/', ServiceListAPIView.as_view(), name='search'),
    # ---------------------
    # orders
    path('order/<int:pk>/', OrderRetriewAPIView.as_view(), name='retrieve-order'),
    path('quote/create/', QuoteCreateAPIView.as_view(), name='create-quote'),
    path('quote/delete/<str:uidb64>/<str:token>/<int:quote_id>/', QuoteDeleteView.as_view(), name='delete-quotation'),
    # ---------------------
    # cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart-item/', CartItemAPIView.as_view(), name='create-cart-item'),
    path('cart-item/<int:pk>/', CartItemDestroyAPIView.as_view(), name='destroy-cart-item'),
    path('cart-detail/', CartAPIView.as_view(), name='cart-detail'),
    # ---------------------
    # checkout
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout-quote/<int:quote>/', QuoteCheckoutView.as_view(), name='quote-checkout'),
]
