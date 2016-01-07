from django.conf.urls import patterns, include, url
from library.views import BookList, BookDetail, AuthorList, AuthorDetail, Catalog, Index, BookishLogin, BookishUpload 


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bookServer.views.home', name='home'),
    # url(r'^bookServer/', include('bookServer.foo.urls')),
    url(r'^books/$', BookList.as_view()),
    url(r'^books/(.+?)/$', BookDetail.as_view()),
    url(r'^authors/$', AuthorList.as_view()),
    url(r'^authors/(.+?)/$', AuthorDetail.as_view()),
    url(r'^index/$', Index.as_view()),
    url(r'^bookish/user$', BookishLogin.as_view()),
    url(r'^bookish/book$', BookishUpload.as_view()), 
    url(r'^$', Catalog.as_view()),
    url(r'^cat', TemplateView.as_view(template_name='static/library/public/views/landing.html'),name='cat'),
)
