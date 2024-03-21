from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "django_app/registration/signup.html"


class LoginView(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("django_app:dashboard")
    template_name = "django_app/registration/login.html"
