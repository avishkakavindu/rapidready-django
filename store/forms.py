from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from store.models import User, Review


class SignUpForm(UserCreationForm):
    """ Signup form """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class AddToCartForm(forms.Form):
    """ Add a service to cart form """

    quantity = forms.IntegerField(validators=[MinValueValidator(1)], required=True)


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
