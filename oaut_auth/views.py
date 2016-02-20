import os
import httplib2
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_orm import Storage
 
from apiclient.discovery import build
 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site
 
from .models import CredentialsModel, FlowModel
 
CLIENT_SECRETS = os.path.join(
    os.path.dirname(__file__), 'client_secrets.json')
 
 
def get_accounts_ids(service):
    accounts = service.management().accounts().list().execute()
    ids = []
    if accounts.get('items'):
        for account in accounts['items']:
            ids.append(account['id'])
    return ids
 
 
@login_required
def index(request):
    # use the first REDIRECT_URI if you are developing your app
    # locally, and the second in production
    # REDIRECT_URI = 'http://localhost:8000/oauth2/oauth2callback'
    REDIRECT_URI = "https://%s%s" % (
        get_current_site(request).domain, reverse("oauth2:return"))
    FLOW = flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/books',
        redirect_uri=REDIRECT_URI
    )
    user = request.user
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid is True:
        FLOW.params['state'] = xsrfutil.generate_token(
            settings.SECRET_KEY, user)
        FLOW.params['next'] = request.GET.get('next')
        authorize_url = FLOW.step1_get_authorize_url()
        f = FlowModel(id=user, flow=FLOW)
        f.save()
        return HttpResponseRedirect(authorize_url)
    else:
        return HttpResponse('<html><head><title>Close</title></head><body onload="window.close();">Thank you for authorizing the app. Please close this window</body></html>')
 
 
@login_required
def auth_return(request):
    user = request.user
    FLOW = FlowModel.objects.get(id=user).flow
    if not xsrfutil.validate_token(
            settings.SECRET_KEY, FLOW.params['state'], user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET['code'])
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect(reverse("oauth2:index"))