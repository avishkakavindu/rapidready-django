from django.contrib.auth.forms import UserCreationForm
from django import forms
from store.models import User


class SignUpForm(UserCreationForm):
    """ Signup form """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

