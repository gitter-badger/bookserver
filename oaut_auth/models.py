from django.db import models
from django.contrib.auth.models import User
from oauth2client.contrib.django_orm import FlowField, CredentialsField
 
 
class FlowModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    flow = FlowField()
 
 
class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()