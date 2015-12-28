from django.db import models
from myUtils import unique_slugify
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey('Publisher', blank=True,  null = True)
    series = models.ManyToManyField('Series', through='book_series', blank=True,  null = True)
    parse_string = models.CharField(max_length=512)
    tags = models.ManyToManyField('Tag', blank=True,  null = True)
    slug = models.SlugField(blank=True, null = True)
    isbn = models.DecimalField(decimal_places=0, max_digits=13, blank=True, null = True)
    def save_path_cover(instance, filename):
        fname, dot, extension = filename.rpartition('.')
        path = instance.title
        path = 'bookCovers/' + path
        return '%s.%s' % (path, extension)
    fileTypes = models.ManyToManyField('FileType', through='BookFile')
    cover = models.ImageField(upload_to=save_path_cover, blank=True, max_length=512)
    def save_path(instance, filename):
        fname, dot, extension = filename.rpartition('.')
        slug = instance.book.title
        return '%s.%s' % (slug, extension) 
    def save(self, *args, **kwargs):
        unique_slugify(self, self.title) 
        super(Book, self).save(*args, **kwargs)
    def __unicode__(self):
        return self.title
    def as_dict(self):
        return {
            'id':self.id,
            'title':self.title,
            'authors':[model_to_dict(author) for author in self.authors.all()],
            'publisher':self.publisher,
            'series':[model_to_dict(series) for series in self.series.all()],
            'tags':[model_to_dict(tag) for tag in self.tags.all()],
            'slug':self.slug,
            'isbn':self.isbn,
            'filetypes':[model_to_dict(filetype) for filetype in self.fileTypes.all()],
            'coverurl':self.cover.url
            }
class book_series(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey('Book')
    series = models.ForeignKey('Series')
    bookNumber = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null = True)

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    sort = models.CharField(max_length=255, unique=True)
    def __unicode__(self):
        return self.name
    
class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    def __unicode__(self):
        return self.name
    
class Series(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    authors = models.ManyToManyField(Author)
    summary = models.TextField(blank = True)
    def __unicode__(self):
        return self.name
    
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return self.text

class FileType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=5)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return self.name
    
class BookFile(models.Model):
    book = models.ForeignKey(Book)
    fileType = models.ForeignKey(FileType)
    def save_path(instance, filename):
        fname, dot, extension = filename.rpartition('.')
        slug = instance.book.title
        return '%s.%s' % (slug, extension) 
    fileLocation = models.FileField(upload_to=save_path, max_length=256)
    def __unicode__(self):
        return self.book.title + ' ' + self.fileType.name   
        
class Bookish(models.Model):
    user = models.OneToOneField(User)
    login_cookie = models.CharField(max_length=512, blank=True)
