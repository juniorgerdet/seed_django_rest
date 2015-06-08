#title           :pyscript.py
#description     :Extend letucce for implemented BDD on Django.
#author          :juniorgerdet
#date            :04-06-2015
#version         :0.1
#usage           :python manager harvest
#notes           :
#python_version  :2.7.10  
#==============================================================================
from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta, datetime
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User)
    role_alt = models.CharField(max_length=256, null=False)
    phone=models.CharField(max_length=50, blank=True)

class Driver(models.Model):
    user = models.OneToOneField(User)
    license_plate = models.CharField(max_length=10, blank=True)
    busy = models.BooleanField(default=0)

class Ride(models.Model):
    id = models.AutoField(primary_key=True)
    taxi_driver = models.ForeignKey(User, blank=True, null=True, related_name='drives')
    client = models.ForeignKey(User, blank=True, null=True, related_name='clients')
    origin = models.CharField(max_length=256, blank=True)
    destiny = models.CharField(max_length=512, blank=True)
    active =  models.BooleanField(default=1)
    create_time =models.DateTimeField(default=timezone.now, editable=False, blank=True, null=True)
