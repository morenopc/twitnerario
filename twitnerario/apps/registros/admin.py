# -*- coding: UTF8 -*-
from django.contrib import admin
from registros.models import Registros

class RegistrosAdmin(admin.ModelAdmin):
    list_display=('twitter','ponto','linha','horas','minutos','lembrar','criado_em')
    #list_display_links = ('id', 'nome')
    search_fields=['twitter','ponto','linha']
    list_filter=('criado_em',)
    #date_hierarchy = 'criado_em'
    #ordering = ['-cad_bl1Data']

admin.site.register(Registros, RegistrosAdmin)
