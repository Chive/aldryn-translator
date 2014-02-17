# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Renaming field 'TranslationRequest.all_stacks' to 'TranslationRequest.all_static_placeholders'
        db.rename_column(u'aldryn_translator_translationrequest', 'all_stacks', 'all_static_placeholders')

    def backwards(self, orm):
        # Renaming field 'TranslationRequest.all_static_placeholders' to 'TranslationRequest.all_stacks'
        db.rename_column(u'aldryn_translator_translationrequest', 'all_static_placeholders', 'all_stacks')

    models = {
        u'aldryn_translator.translationrequest': {
            'Meta': {'object_name': 'TranslationRequest'},
            'all_pages': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'all_static_placeholders': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'copy_content': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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