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
    status = models.CharField(default='active')
    created_by = models.ForeignKey('app2.User', on_delete=models.CASCADE)
    winner_painting = models.ForeignKey(Painting, on_delete=models.CASCADE)
    class Meta:
        model = Exhibition
        fields = ['name', 'theme', 'description', 'start_date', 'end_date', 'status', 'created_by', 'winner_painting']
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