from django import forms
from django.db import models

import app2
from .models import Exhibition, User, Painting

class Theme(models.TextChoices):
    PRIRODA = ('priroda', 'Priroda')
    PORTRET = ('portret', 'Portret')
    ARHITEKTURA = ('arhitektura', 'Arhitektura')
    SLOBODNA = ('slobodna', 'Slobodna tema')


class ExhibitionForm(forms.ModelForm):
    name = models.CharField(max_length=120)
    theme = models.CharField(choices=Theme.choices)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        model = Exhibition
        fields = ['name', 'theme', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

#class ExhibitionFormFront(forms.ModelForm):
   #THEME_CHOICES = [
       #('priroda', 'Priroda'),
        #('portret', 'Portret'),
        #('arhitektura', 'Arhitektura'),
        #('slobodna', 'Slobodna tema'),
    #]

    #theme = forms.ChoiceField(choices=THEME_CHOICES, required=True)

    #class Meta:
        #model = Exhibition
        #fields = ['name', 'theme', 'description', 'start_date', 'end_date']
        #widgets = {
            #'start_date': forms.DateInput(attrs={'type': 'date'}),
            #'end_date': forms.DateInput(attrs={'type': 'date'}),
            #'description': forms.Textarea(attrs={'rows': 3}),
        #}