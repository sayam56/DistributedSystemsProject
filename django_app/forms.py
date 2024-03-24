from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]


class StockSearch(forms.Form):
    q = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control me-2', 'type': 'search', 'placeholder': 'Stock Symbol', 'aria-label': 'Search'}))



class SearchForm(forms.Form):
    TickerName = forms.CharField(max_length=100,required=True)
    NumberofDays = forms.IntegerField(required=True)