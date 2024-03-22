from django import forms

from django_app.models import News


class SearchForm(forms.Form):
    TickerName = forms.CharField(max_length=100,required=True)
    NumberofDays = forms.IntegerField(required=True)


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'author', 'date']
