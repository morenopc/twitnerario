# -*- coding: UTF8 -*-
from django.contrib import admin
from core.models import Configuracao


class ConfiguracaoAdmin(admin.ModelAdmin):
    """Configuração admin """
    list_display = ('descricao', 'previsao_origin', 'previsao_pathname',
        'previsao_js', 'pontos_pathname', 'linhas_pathname')

admin.site.register(Configuracao, ConfiguracaoAdmin)
