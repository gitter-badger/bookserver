
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
import httplib2
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_orm import Storage
 
from apiclient.discovery import build


from __future__ import unicode_literals

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.db.models import Q, Max
from django.db.models.base import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings

from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from itertools import chain
from library.models import Book, Author, Series, BookFile,Bookish
from library.myUtils import extract_form_fields
from oaut_auth.models import CredentialsModel, FlowModel
from random import shuffle, randint
import requests as basic_request
import re
import urllib
import urllib2
import json

import httplib2
import pprint


from django.core.files.base import ContentFile


class AuthorList(ListView):
    queryset = Author.objects.order_by('sort')
    
class AuthorDetail(DetailView):
    model = Author
    
class BookList(ListView):
    queryset = Book.objects.order_by('title')

class BookDetail(DetailView):
    def get_object(self):
        self.book = get_object_or_404(Book, slug=self.args[0])
        return self.book
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BookDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['bookFiles'] = BookFile.objects.filter(book = self.book)
        return context

class Catalog(ListView):

    template_name = 'library/catalog.html'

    def get_queryset(self):
        return 1


class Index(View):
    def get(self, request):
        search_term = request.GET.get('s', '')
        search_words = search_term.split(' ')
        filter_search = ' '.join(search_words[1:])
        rand_ids = []
        if (search_words[0] == "<random>"):
            total_items = Book.objects.aggregate(Max('id'))['id__max']
            for x in range (0, int(search_words[1])):
                rand_ids.append(randint(0,total_items))
            
            result_list = Book.objects.filter(id__in=rand_ids)
        elif (search_words[0] == "<Author>"):
            result_list = Book.objects.filter(authors__name=filter_search)
        elif (search_words[0] == "<Title>"):
            result_list = Book.objects.filter(title=filter_search)
        elif (search_words[0] == "<Series>"):
            result_list = Book.objects.filter(series__name=filter_search)
        else:
            result_list = Book.objects.filter(Q(title__icontains=search_term) | Q(authors__name__icontains=search_term) | Q(series__name__icontains=search_term)).distinct()
        coverData =[]
        for book in result_list:
            coverData.append("Has Cover")
            if book.cover == 'none':
                coverData[-1] = "Missing Cover Added"
                title=urllib.quote(book.title)
                author=urllib.quote(book.authors.first().name)
                myUrl="https://www.googleapis.com/books/v1/volumes?q=intitle:%s+inauthor:%s&startIndex=0&maxResults=1&key=%s"%(title,author,settings.GOOGLE_BOOKS_API_KEY)
                response = basic_request.get(myUrl)
                data = json.loads(response.text)
                if 'totalItems' not in data:
                    coverData[-1] = "API Limit"
                    continue
                if not data['totalItems'] :
                    coverData[-1] = "Book not Found"
                    book.cover = "none_google"
                    book.save()
                    continue
                bookData = data['items'][0]['volumeInfo']
                if 'imageLinks' in bookData:
                    image_content = ContentFile(basic_request.get(bookData['imageLinks']['thumbnail']).content)
                    book.cover.save("cover.jpg", image_content)
                else:
                    coverData[-1] = "No Covers at Google"
                    book.cover = "none_google"
                    book.save()
                    continue
        rawdata = [obj.as_dict() for obj in result_list]
        serialized_data = json.dumps({'Test':coverData, 'rawdata':rawdata})
        return HttpResponse(serialized_data, content_type="application/json")
    def post(self, request):
        #Need to pull search term here filter author, series, and title off 
        #of it and then compiler dataset for templates
        search_term = request.POST.get('searchdata', '')
        search_words = search_term.split(' ')
        filter_search = ' '.join(search_words[1:])
        rand_ids = []
        if (search_words[0] == "<random>"):
            total_items = Book.objects.aggregate(Max('id'))['id__max']
            for x in range (0, int(search_words[1])):
                rand_ids.append(randint(0,total_items))
            
            result_list = Book.objects.filter(id__in=rand_ids)
        elif (search_words[0] == "<Author>"):
            result_list = Book.objects.filter(authors__name=filter_search)
        elif (search_words[0] == "<Title>"):
            result_list = Book.objects.filter(title=filter_search)
        elif (search_words[0] == "<Series>"):
            result_list = Book.objects.filter(series__name=filter_search)
        else:
            result_list = Book.objects.filter(Q(title__icontains=search_term) | Q(authors__name__icontains=search_term) | Q(series__name__icontains=search_term)).distinct()
        booklist = render_to_string('library/booklistCompiler.html', {'object_list': result_list})
        carousel = render_to_string('library/carouselCompiler.html', {'object_list': result_list})
        
        rawdata = [obj.as_dict() for obj in result_list]
        serialized_data = json.dumps({'booklist': booklist, 'carousel': carousel,'rawdata':rawdata})
        return HttpResponse(serialized_data, content_type="application/json")


class BookishLogin(View):
    def get(self, request):
        thisUser = User.objects.filter(id = request.user.id)[0]
        askLogin = True
        try:
            if thisUser.bookish and thisUser.bookish.login_cookie:
                askLogin = False
        except ObjectDoesNotExist:
            askLogin = True
        serialized_data = json.dumps({'askLogin': askLogin})
        return HttpResponse(serialized_data, content_type="application/json")
    
    def post(self, request):
        url = 'https://booki.sh/sign/in'
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
        user = request.POST.get('username')
        passwd = request.POST.get('password')
        #r = urllib2.urlopen("https://booki.sh/")
        #data = r.read()
        #cookies = r.info()['Set-Cookie']
        #soup = BeautifulSoup(data)
        #encodingTag = soup.find('input', {"name":'utf8'})
        #token = soup.find('input', {"name":"authenticity_token"})
        values = {'account[email]' : user, 'account[password]' : passwd}
        data2 = urllib.urlencode(values)
        #headers = {'User-Agent' : user_agent, 'Host': 'booki.sh', 'Connection': 'keep-alive', 
        #            'Content-Length': '80', 'Cache-Control': 'max-age=0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #           'Origin': 'null','Content-Type': 'application/x-www-form-urlencoded', 'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-US,en;q=0.8,es;q=0.6'}
       
        headers = {'User-Agent' : user_agent}
        response = basic_request.post(url, data = data2, headers = headers)
        the_page = response.text
        cookies = response.cookies
        cookiesDefined = basic_request.utils.dict_from_cookiejar(cookies)
        if 'remtok' in cookiesDefined:
            cookies = cookiesDefined['remtok']
            thisUser = User.objects.filter(id = request.user.id)[0]
            try:
                if thisUser.bookish and thisUser.bookish.login_cookie:
                    thisUser.bookish.login_cookie = cookies
                    thisUser.save()
            except ObjectDoesNotExist:
                thisAccount = Bookish(user=thisUser, login_cookie=cookies)
                thisAccount.save()
            serialized_data = json.dumps({'cookies': cookies, 'save_cookie':thisUser.bookish.login_cookie})
        else:
            serialized_data = json.dumps({'remtok': 'Invalid', 'cookies': cookiesDefined, 'page':the_page, 'data':data2})
        return HttpResponse(serialized_data, content_type="application/json")
        
class BookishUpload(View):
    def post(self, request):
        thisUser = User.objects.filter(id = request.user.id)[0]
        remtok = {'remtok': thisUser.bookish.login_cookie}
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
        upload_url = "https://booki-sh-possessions-incoming.s3.amazonaws.com"
        headers = {'User-Agent' : user_agent}
        response = basic_request.get('https://booki.sh/library/upload', headers = headers, cookies=remtok)
        cookies = response.cookies
        the_page = response.text
        soup = BeautifulSoup(the_page)
        form = extract_form_fields(soup)
        if 'commit' in form:
            if form['commit'] == "Sign in":
                serialized_data = json.dumps({'askLogin': True, 'remtok': remtok})
                return HttpResponse(serialized_data, content_type="application/json")

        form['file'] = open('c:\\media_root\\' + request.POST.get('filename'), 'rb')
        form2 = form.items()
        fileindex = [i for i, v in enumerate(form2) if v[0] == 'file']
        form2.append(form2.pop(fileindex[0]))
        result = basic_request.post(upload_url, files=form2, allow_redirects=False, headers=headers)
        result2 = basic_request.get(result.headers['location'], headers = headers, cookies=cookies)
        status = re.findall('status\\\":\\\"(.*?)\\\",',result2.text)
        serialized_data = json.dumps({'status':status})
        #serialized_data = json.dumps({"test":"success"})
        return HttpResponse(serialized_data, content_type="application/json")
            
class Autocomplete(View):
    def get(self, request):
        here = 0
        search_term = request.GET.get('s', '')
        search_words = search_term.split(' ')
        filter_search = ' '.join(search_words[1:])
        rand_ids = []
        result_list = None
        if search_words[0].startswith('<'):
            if (search_words[0] in "<random>"):
                total_items = Book.objects.aggregate(Max('id'))['id__max']
                if len(search_words) > 1 and int(search_words[1]) < total_items:
				    result_list =['<random> %s' %filter_search]
                else: 
				    result_list =['<random> %d' %total_items]
            elif (search_words[0] in "<Author>" or search_words[0] in "<author>"):
                here = 1
                result_list = ["<Author> %s" %author.name for author in Author.objects.filter(name__istartswith=filter_search)[:2]] + \
                              ["<Author> %s" %author.sort for author in Author.objects.filter(sort__istartswith=filter_search)[:1]]
            elif (search_words[0] in "<Title>" or search_words[0] in "<title>"):
                result_list = ["<Title> %s" %book.title for book in Book.objects.filter(title__istartswith=filter_search)[:4]]
            elif (search_words[0] in "<Series>" or search_words[0] in "<series>"):
                result_list = ["<Series> %s"%series.name for series in series.objects.filter(name__istartswith=filter_search)[:4]]
        if not result_list:
            here = 2
            result_list = [author.name for author in Author.objects.filter(name__istartswith=search_term)[:2]] + \
                          [author.sort for author in Author.objects.filter(sort__istartswith=search_term)[:1]] + \
		                  [book.title for book in Book.objects.filter(title__istartswith=search_term)[:2]] + \
				    	  [series.name for series in Series.objects.filter(name__istartswith=search_term)[:1]]
        serialized_data = json.dumps({"result_list":result_list,'debug':{'test':here, 'search_term':search_term,'search_words':search_words}})
        return HttpResponse(serialized_data, content_type="application/json")    
        
class BookUpload(View):
    def get(self, request):
        file_id = request.GET.get('fileid')
        user = request.user
        storage = Storage(CredentialsModel, 'id', user, 'credential')
        credential = storage.get()
        if credential is None or credential.invalid is True:
            return HttpResponse(json.dumps({'authorize_url':reverse("oauth2:index"), 'recall_url':"%s?fileid=%s"%(reverse("library:upload"),file_id)}),content_type="application/json")
        http = httplib2.Http()
        http = credential.authorize(http)
        drive_service = build('drive', 'v2', http=http)
        books_service = build('books', 'v1', http=http)
        
        bookfile = get_object_or_404(BookFile, id=file_id)
        # Insert a file
        media_body = MediaFileUpload(bookfile.fileLocation.path, mimetype='application/epub+zip')
        body = {
            'title': bookfile.book.title,
        }
        file = drive_service.files().insert(body=body, media_body=media_body).execute()
 
        # Add a book to the shelf
        book = books_service.cloudloading().addBook(drive_document_id=file['id']).execute()
        return HttpResponse(json.dumps(book))
        
    
    
    
    
    
    
