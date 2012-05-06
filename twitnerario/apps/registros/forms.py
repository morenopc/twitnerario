# -*- coding: UTF8 -*-

from django import forms
from django.forms import ModelForm
from form_utils.forms import BetterModelForm
from registros.models import Registros

class RegistrosForm(BetterModelForm):
    class Meta:
        model=Registros
        widgets = {
            'linha':forms.Select(),
            'fim_de_semana':forms.TextInput(attrs={'style': 'display:none'}),
        }
        fieldsets=[
                   ('Registro', {
                   'fields': [
                              'twitter',
                              'ponto',
                              'linha',
                              'horas',
                              'minutos',
                              'lembrar',
                              'fim_de_semana',
                              ],
                   'classes': ['registro']
                   })
                 ]
        row_attrs = {
        }
        
