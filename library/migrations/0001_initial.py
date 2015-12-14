# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Book'
        db.create_table(u'library_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Publisher'], null=True, blank=True)),
            ('parse_string', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('isbn', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=0, blank=True)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'library', ['Book'])

        # Adding M2M table for field authors on 'Book'
        m2m_table_name = db.shorten_name(u'library_book_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm[u'library.book'], null=False)),
            ('author', models.ForeignKey(orm[u'library.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'author_id'])

        # Adding M2M table for field tags on 'Book'
        m2m_table_name = db.shorten_name(u'library_book_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm[u'library.book'], null=False)),
            ('tag', models.ForeignKey(orm[u'library.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'tag_id'])

        # Adding model 'book_series'
        db.create_table(u'library_book_series', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Book'])),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Series'])),
            ('bookNumber', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'library', ['book_series'])

        # Adding model 'Author'
        db.create_table(u'library_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('sort', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'library', ['Author'])

        # Adding model 'Publisher'
        db.create_table(u'library_publisher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'library', ['Publisher'])

        # Adding model 'Series'
        db.create_table(u'library_series', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'library', ['Series'])

        # Adding M2M table for field authors on 'Series'
        m2m_table_name = db.shorten_name(u'library_series_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('series', models.ForeignKey(orm[u'library.series'], null=False)),
            ('author', models.ForeignKey(orm[u'library.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['series_id', 'author_id'])

        # Adding model 'Tag'
        db.create_table(u'library_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'library', ['Tag'])

        # Adding model 'FileType'
        db.create_table(u'library_filetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'library', ['FileType'])

        # Adding model 'BookFile'
        db.create_table(u'library_bookfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Book'])),
            ('fileType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.FileType'])),
            ('fileLocation', self.gf('django.db.models.fields.files.FileField')(max_length=256)),
        ))
        db.send_create_signal(u'library', ['BookFile'])


    def backwards(self, orm):
        # Deleting model 'Book'
        db.delete_table(u'library_book')

        # Removing M2M table for field authors on 'Book'
        db.delete_table(db.shorten_name(u'library_book_authors'))

        # Removing M2M table for field tags on 'Book'
        db.delete_table(db.shorten_name(u'library_book_tags'))

        # Deleting model 'book_series'
        db.delete_table(u'library_book_series')

        # Deleting model 'Author'
        db.delete_table(u'library_author')

        # Deleting model 'Publisher'
        db.delete_table(u'library_publisher')

        # Deleting model 'Series'
        db.delete_table(u'library_series')

        # Removing M2M table for field authors on 'Series'
        db.delete_table(db.shorten_name(u'library_series_authors'))

        # Deleting model 'Tag'
        db.delete_table(u'library_tag')

        # Deleting model 'FileType'
        db.delete_table(u'library_filetype')

        # Deleting model 'BookFile'
        db.delete_table(u'library_bookfile')


    models = {
        u'library.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'sort': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'library.book': {
            'Meta': {'object_name': 'Book'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['library.Author']", 'symmetrical': 'False'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'fileTypes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['library.FileType']", 'through': u"orm['library.BookFile']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '0', 'blank': 'True'}),
            'parse_string': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['library.Publisher']", 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['library.Series']", 'null': 'True', 'through': u"orm['library.book_series']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['library.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'library.book_series': {
            'Meta': {'object_name': 'book_series'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['library.Book']"}),
            'bookNumber': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['library.Series']"})
        },
        u'library.bookfile': {
            'Meta': {'object_name': 'BookFile'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['library.Book']"}),
            'fileLocation': ('django.db.models.fields.files.FileField', [], {'max_length': '256'}),
            'fileType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['library.FileType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'library.filetype': {
            'Meta': {'object_name': 'FileType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'library.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'library.series': {
            'Meta': {'object_name': 'Series'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['library.Author']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'library.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['library']