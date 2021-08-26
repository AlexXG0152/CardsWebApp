from django.forms import ModelForm, widgets
from django import forms
from . import models

from crispy_forms.helper import FormHelper


class CardEditForm(ModelForm):
    class Meta:
        model = models.Card 
        fields = ['series', 'number', 'date_start',
                  'date_end', 'date_delete', 'period', 'status']
        widgets = {
            'date_start': widgets.DateInput(attrs={'type': 'date'})
        }


class AuthorListFormHelper(FormHelper):
    model = models.Card 
    form_tag = False


class GenerateCards(forms.Form):
    series = forms.CharField(label="Series", max_length=2, widget=forms.TextInput(attrs={'placeholder': 'max 2 symbols'}))
    quantity = forms.CharField(label="Quantity", max_length=5, widget=forms.TextInput(attrs={'placeholder': 'max 5 symbols'}))
    status = forms.CharField(label="Status",max_length=1, widget=forms.Select(choices=models.Card.CARD_STATUS))
    period = forms.CharField(label="How_long",max_length=3, widget=forms.Select(choices=models.Card.CARD_PERIOD))
    
    class Meta:
        model = models.Card 
        fields = ['series', 'number', 'status', 'period']
