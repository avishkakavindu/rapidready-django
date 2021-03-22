from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

# make 'User' refers to custom User instead of default django.contrib.auth.models.user
User = get_user_model()


def login(request):
    print('\n\n\njj\n\n\n')
    context = {
        'error': False,
        'is_active': 'True',
        'email': ''
    }
    if request.method == 'POST':
        username_or_email = request.POST['username']

        try:
            # get username by email
            username = User.objects.get(email=username_or_email).username
        except User.DoesNotExist:
            username = request.POST['username']

        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, "Login successfull")
            return redirect('profile')
        else:
            try:
                user = User.objects.get(username=username)

                if user.is_active:
                    messages.error(request, 'Invalid credentials, \nPlease check username/email or password.')
                    context['error'] = True
                else:
                    context['error'] = True
                    context['is_active'] = False
                    context['email'] = User.objects.get(username=username).email
                    messages.error(request, 'Inactive account detected, \nPlease please verify your email address.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid credentials, \nPlease check username/email or password.')
                context['error'] = True

    return render(request, "registration/login.html", context=context)