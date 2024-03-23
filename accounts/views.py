from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from accounts.forms import UserProfileForm, UserSignupForm


# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "django_app/registration/signup.html"

def SignUpView(request):
    if request.method == 'POST':
        user_form = UserSignupForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)  # Include request.FILES for image uploads
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            success_url = reverse_lazy("login")
            # Redirect to a success page or login the user
            return redirect('login')
    else:
        user_form = UserSignupForm()
        profile_form = UserProfileForm()

    return render(request, 'django_app/registration/signup.html',
                  {'user_form': user_form, 'profile_form': profile_form})


class LoginView(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("django_app:dashboard")
    template_name = "django_app/registration/login.html"
