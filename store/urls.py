from django.contrib.auth import views as auth_views
from django.urls import path

from store.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', auth_views.LoginView.as_view( redirect_authenticated_user=True), name='login'),

    path(
        'password_reset',
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',
                                             html_email_template_name="registration/password_reset_email.html",
                                             # email_template_name='registration/password_reset_email.html',
                                             ),
        name='password_reset'
    ),  # allows a user to reset their password by generating a one-time use link
    path(
        'password_reset_done',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),  # after password reset email sent
]
