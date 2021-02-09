from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.shortcuts import render


class CustomLoginView(LoginView):
    pass
    # template_name = 'accounts/login.html'
    # redirect_authenticated_user = True
    # form_class = LoginForm
