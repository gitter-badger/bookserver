from django.contrib import admin
from library.models import *

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Series)
admin.site.register(Tag)
admin.site.register(FileType)
admin.site.register(BookFile)
