from django import forms


class SearchForm(forms.Form):
    TickerName = forms.CharField(max_length=100,required=True)
    NumberofDays = forms.IntegerField(required=True)


