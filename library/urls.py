from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from library.views import * 


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
    url(r'^cat/$', Catalog.as_view()),
	url(r'^auto/$', Autocomplete.as_view()),
    url(r'^upload/$', BookUpload.as_view(),name='upload'),
    url(r'^$', TemplateView.as_view(template_name='library/angularCatalog.html'),name='cat'),
)
