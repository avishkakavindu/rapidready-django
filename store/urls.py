from django.contrib.auth import views as auth_views
from django.urls import path

from store.views import HomeView, SignUpView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('register', SignUpView.as_view(), name='register'),

    # password reset paths
    path(
        'password_reset',
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',
                                             html_email_template_name="registration/password_reset_email.html",
                                             email_template_name='registration/password_reset_email.html',
                                             ),
        name='password_reset'
    ),  # allows a user to reset their password by generating a one-time use link
    path(
        'password_reset_done',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),  # after password reset email sent
    path(
        'password_reset_confirm/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),  # present a form to enter new password
    path(
        'password_reset_complete',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'
    ),  # inform success

]
