# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from coop_cms.settings import COOP_CMS_NAVTREE_CLASS, DEPRECATED_COOP_CMS_NAVTREE_CLASS

NAVTREE_CLASS = DEPRECATED_COOP_CMS_NAVTREE_CLASS or COOP_CMS_NAVTREE_CLASS

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NavTree'
        db.create_table(u'coop_cms_navtree', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='default', unique=True, max_length=100, db_index=True)),
        ))
        db.send_create_signal(u'coop_cms', ['NavTree'])

        # Adding M2M table for field types on 'NavTree'
        m2m_table_name = db.shorten_name(u'coop_cms_navtree_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('navtree', models.ForeignKey(orm[u'coop_cms.navtree'], null=False)),
            ('navtype', models.ForeignKey(orm[u'coop_cms.navtype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['navtree_id', 'navtype_id'])

        # Deleting field 'NavNode.tree'
        db.delete_column(u'coop_cms_navnode', 'tree_id')


    def backwards(self, orm):
        # Deleting model 'NavTree'
        db.delete_table(u'coop_cms_navtree')

        # Removing M2M table for field types on 'NavTree'
        db.delete_table(db.shorten_name(u'coop_cms_navtree_types'))

        # User chose to not deal with backwards NULL issues for 'NavNode.tree'
        raise RuntimeError("Cannot reverse this migration. 'NavNode.tree' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'NavNode.tree'
        db.add_column(u'coop_cms_navnode', 'tree',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm[NAVTREE_CLASS]),
                      keep_default=False)


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'coop_cms.alias': {
            'Meta': {'object_name': 'Alias'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'redirect_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        u'coop_cms.articlecategory': {
            'Meta': {'object_name': 'ArticleCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_rss': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'default': '[1]', 'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '100', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'})
        },
        u'coop_cms.document': {
            'Meta': {'object_name': 'Document'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['coop_cms.ArticleCategory']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filters': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': u"orm['coop_cms.MediaFilter']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        },
        u'coop_cms.fragment': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'Fragment'},
            'content': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'css_class': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '100', 'blank': 'True'}),
            'filter': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['coop_cms.FragmentFilter']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coop_cms.FragmentType']"})
        },
        u'coop_cms.fragmentfilter': {
            'Meta': {'object_name': 'FragmentFilter'},
            'extra_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'coop_cms.fragmenttype': {
            'Meta': {'object_name': 'FragmentType'},
            'allowed_css_classes': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        u'coop_cms.image': {
            'Meta': {'object_name': 'Image'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'filters': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': u"orm['coop_cms.MediaFilter']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['coop_cms.ImageSize']", 'null': 'True', 'blank': 'True'})
        },
        u'coop_cms.imagesize': {
            'Meta': {'object_name': 'ImageSize'},
            'crop': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'coop_cms.link': {
            'Meta': {'object_name': 'Link'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'title'", 'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'coop_cms.mediafilter': {
            'Meta': {'object_name': 'MediaFilter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'coop_cms.navnode': {
            'Meta': {'object_name': 'NavNode'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['coop_cms.NavNode']", 'null': 'True', 'blank': 'True'}),
            'tree_value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'coop_cms.navtree': {
            'Meta': {'object_name': 'NavTree'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'default'", 'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'coop_cms_navtree_set'", 'blank': 'True', 'to': u"orm['coop_cms.NavType']"})
        },
        u'coop_cms.navtype': {
            'Meta': {'object_name': 'NavType'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_rule': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'search_field': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        u'coop_cms.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            'content': ('django.db.models.fields.TextField', [], {'default': "'<br>'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['coop_cms.NewsletterItem']", 'symmetrical': 'False', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'source_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        u'coop_cms.newsletteritem': {
            'Meta': {'ordering': "['ordering']", 'unique_together': "(('content_type', 'object_id'),)", 'object_name': 'NewsletterItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'coop_cms.newslettersending': {
            'Meta': {'object_name': 'NewsletterSending'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newsletter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coop_cms.Newsletter']"}),
            'scheduling_dt': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'sending_dt': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'coop_cms.pieceofhtml': {
            'Meta': {'object_name': 'PieceOfHtml'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'div_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'extra_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'coop_cms.sitesettings': {
            'Meta': {'ordering': "('site__id',)", 'object_name': 'SiteSettings'},
            'homepage_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sites.Site']", 'unique': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['coop_cms']