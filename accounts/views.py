from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
# from accounts.forms import UserCreationForm


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# def SignUpView(request):
#     if request.method == 'POST':
#         user_form = UserSignupForm(request.POST)
#         profile_form = UserProfileForm(request.POST, request.FILES)  # Include request.FILES for image uploads
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
#             success_url = reverse_lazy("login")
#             # Redirect to a success page or login the user
#     else:
#         user_form = UserSignupForm()
#         profile_form = UserProfileForm()
#
#     return render(request, 'registration/signup.html', {'user_form': user_form, 'profile_form': profile_form})