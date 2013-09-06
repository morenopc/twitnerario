# -*- coding: UTF8 -*-

from django import forms
from django.forms import ModelForm
from form_utils.forms import BetterModelForm
from registros.models import Registros


class RegistrosForm(BetterModelForm):
    """Formulário de registros de tweets"""

    class Meta:
        model = Registros
        
        fieldsets = [
            ('Registro', {
                'fields': ('twitter', 'ponto', 'linha', 'horas',
                            'minutos', 'lembrar', 'fim_de_semana'),
                'classes': ['registro']
                })
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrosForm, self).__init__(*args, **kwargs)

        self.fields['linha'].widget = forms.Select()
        self.fields['fim_de_semana'].widget.attrs = {
            'style': 'display:none'}

    def clean(self):
        twitter = self.cleaned_data.get('twitter')
        linha = self.cleaned_data.get('linha')
        ponto = self.cleaned_data.get('ponto')
        horas = self.cleaned_data.get('horas')
        minutos = self.cleaned_data.get('minutos')
        # Verifica se registro já existe
        if Registros.objects.filter(twitter=twitter, ponto=ponto, linha=linha,
            horas=horas, minutos=minutos).exists():
            raise forms.ValidationError(
                u'Este registro já existe para o twitter {}'.format(twitter))
            
        return self.cleaned_data
