from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta, datetime
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User)
    role_alt = models.CharField(max_length=256, null=False)

class Ride(models.Model):
    id = models.AutoField(primary_key=True)
    taxi_drive = models.ForeignKey(User, blank=True, null=True, related_name='drive_rides')
    client = models.ForeignKey(User, blank=True, null=True, related_name='client_rides')
    origin = models.CharField(max_length=256, blank=True)
    destiny = models.CharField(max_length=512, blank=True)
    active =  models.BooleanField(default=1)
    create_time =models.DateTimeField(default=timezone.now, editable=False, blank=True, null=True)
    
 