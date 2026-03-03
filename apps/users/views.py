from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

class UserLoginView(LoginView):
    template_name='users/login.html'
    authentication_form=CustomAuthenticationForm
