# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TranslationRequest'
        db.create_table(u'aldryn_translator_translationrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('from_lang', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('to_lang', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('status', self.gf('django.db.models.fields.CharField')(default='draft', max_length=30)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=2, blank=True)),
            ('translated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('all_pages', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('all_stacks', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent_content', self.gf('annoying.fields.JSONField')(null=True, blank=True)),
            ('provider', self.gf('django.db.models.fields.CharField')(default='supertext', max_length=100)),
            ('order_choice', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('order_selection', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'aldryn_translator', ['TranslationRequest'])

        # Adding model 'TranslationResponse'
        db.create_table(u'aldryn_translator_translationresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('received_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldryn_translator.TranslationRequest'], null=True, blank=True)),
            ('received_content', self.gf('annoying.fields.JSONField')(null=True, blank=True)),
            ('debug_info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'aldryn_translator', ['TranslationResponse'])


    def backwards(self, orm):
        # Deleting model 'TranslationRequest'
        db.delete_table(u'aldryn_translator_translationrequest')

        # Deleting model 'TranslationResponse'
        db.delete_table(u'aldryn_translator_translationresponse')


    models = {
        u'aldryn_translator.translationrequest': {
            'Meta': {'object_name': 'TranslationRequest'},
            'all_pages': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'all_stacks': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_lang': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_choice': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'order_selection': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'default': "'supertext'", 'max_length': '100'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'sent_content': ('annoying.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '30'}),
            'to_lang': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'translated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'aldryn_translator.translationresponse': {
            'Meta': {'object_name': 'TranslationResponse'},
            'debug_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'received_content': ('annoying.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_translator.TranslationRequest']", 'null': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['aldryn_translator']