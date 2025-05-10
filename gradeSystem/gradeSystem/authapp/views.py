from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
# from django.views import View
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.views import generic
from django.contrib.auth import get_user_model

# Create your views here.

class SignupView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
