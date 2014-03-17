# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventSiteBlock'
        db.create_table(u'siteblocks_eventsiteblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=80, db_index=True)),
            ('template', self.gf('django.db.models.fields.TextField')()),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal(u'siteblocks', ['EventSiteBlock'])


    def backwards(self, orm):
        # Deleting model 'EventSiteBlock'
        db.delete_table(u'siteblocks_eventsiteblock')


    models = {
        u'siteblocks.block': {
            'Meta': {'object_name': 'Block'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'siteblocks.eventsiteblock': {
            'Meta': {'object_name': 'EventSiteBlock'},
            'event': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['siteblocks']