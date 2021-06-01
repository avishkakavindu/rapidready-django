from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from store.models import User, Review, Order


class SignUpForm(UserCreationForm):
    """ Signup form """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class ServiceReviewForm(forms.ModelForm):
    """ Add a review for a service """
    review = forms.CharField(widget=forms.Textarea)
    rating = forms.DecimalField(widget=forms.HiddenInput,
                                max_digits=1,
                                decimal_places=0,
                                validators=[MinValueValidator(0), MaxValueValidator(5)],
                                initial=0)

    class Meta:
        model = Review
        fields = ['review', 'rating']

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating is None:
            return self.field['rating'].initial
        return rating


class OrderReviewForm(forms.ModelForm):
    """ Add a review for a delivered order """
    id = forms.CharField(widget=forms.HiddenInput)
    review = forms.CharField(widget=forms.Textarea)
    rating = forms.DecimalField(widget=forms.HiddenInput,
                                max_digits=1,
                                decimal_places=0,
                                validators=[MinValueValidator(0), MaxValueValidator(5)],
                                initial=0)

    class Meta:
        model = Order
        fields = ['id', 'review', 'rating']

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating is None:
            return self.field['rating'].initial
        return rating


class DeliveryForm(forms.ModelForm):
    """ Add delivery details to the order """

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'desc', 'type', 'status', 'created_on']

