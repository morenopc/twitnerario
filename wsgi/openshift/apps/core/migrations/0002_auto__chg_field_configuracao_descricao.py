# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Configuracao.descricao'
        db.alter_column(u'core_configuracao', 'descricao', self.gf('django.db.models.fields.CharField')(max_length=128))

    def backwards(self, orm):

        # Changing field 'Configuracao.descricao'
        db.alter_column(u'core_configuracao', 'descricao', self.gf('django.db.models.fields.URLField')(max_length=128))

    models = {
        u'core.configuracao': {
            'Meta': {'object_name': 'Configuracao'},
            'descricao': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linhas_pathname': ('django.db.models.fields.CharField', [], {'default': "'pontovitoria/utilidades/listaLinhaPassamNoPonto/'", 'max_length': '128'}),
            'pontos_pathname': ('django.db.models.fields.CharField', [], {'default': "'pontovitoria/utilidades/listaPontos/'", 'max_length': '128'}),
            'previsao_js': ('django.db.models.fields.CharField', [], {'default': "'pontovitoria/js/principal/previsao.js'", 'max_length': '128'}),
            'previsao_origin': ('django.db.models.fields.URLField', [], {'default': "'http://rast.vitoria.es.gov.br/'", 'max_length': '128'}),
            'previsao_pathname': ('django.db.models.fields.CharField', [], {'default': "'pontovitoria/previsao?'", 'max_length': '128'})
        }
    }

    complete_apps = ['core']