from django import forms
from django.db import models

import app2
from .models import Exhibition, User, Painting

"""Enum za teme, kasnije je promenjeno da moze da bude tema bilo sta"""
class Theme(models.TextChoices):
    PRIRODA = ('priroda', 'Priroda')
    PORTRET = ('portret', 'Portret')
    ARHITEKTURA = ('arhitektura', 'Arhitektura')
    SLOBODNA = ('slobodna', 'Slobodna tema')


"""Forma za pravljenje izlozbe"""
class ExhibitionForm(forms.ModelForm):
    name = models.CharField(max_length=120)
    theme = models.CharField(choices=Theme.choices, default=Theme.SLOBODNA)
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

