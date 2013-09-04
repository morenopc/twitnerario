# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Configuracao'
        db.create_table(u'core_configuracao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.URLField')(default='default', max_length=128)),
            ('previsao_origin', self.gf('django.db.models.fields.URLField')(default='http://rast.vitoria.es.gov.br/', max_length=128)),
            ('previsao_pathname', self.gf('django.db.models.fields.CharField')(default='pontovitoria/previsao?', max_length=128)),
            ('previsao_js', self.gf('django.db.models.fields.CharField')(default='pontovitoria/js/principal/previsao.js', max_length=128)),
            ('pontos_pathname', self.gf('django.db.models.fields.CharField')(default='pontovitoria/utilidades/listaPontos/', max_length=128)),
            ('linhas_pathname', self.gf('django.db.models.fields.CharField')(default='pontovitoria/utilidades/listaLinhaPassamNoPonto/', max_length=128)),
        ))
        db.send_create_signal(u'core', ['Configuracao'])


    def backwards(self, orm):
        # Deleting model 'Configuracao'
        db.delete_table(u'core_configuracao')


    models = {
        u'core.configuracao': {
            'Meta': {'object_name': 'Configuracao'},
            'descricao': ('django.db.models.fields.URLField', [], {'default': "'default'", 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linhas_pathname': ('django.db.models.fields.CharField', [], {'default': "'pontovitoria/utilidades/listaLinhaPassamNoPonto/'", 'max_length': '128'}),
            'pontos_pathname': ('django.db.models.fields.CharField', [], {'default': "'pontovitoria/utilidades/listaPontos/'", 'max_length': '128'}),
            'previsao_js': ('django.db.models.fields.CharField', [], {'default': "'pontovitoria/js/principal/previsao.js'", 'max_length': '128'}),
            'previsao_origin': ('django.db.models.fields.URLField', [], {'default': "'http://rast.vitoria.es.gov.br/'", 'max_length': '128'}),
            'previsao_pathname': ('django.db.models.fields.CharField', [], {'default': "'pontovitoria/previsao?'", 'max_length': '128'})
        }
    }

    complete_apps = ['core']