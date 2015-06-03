from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta, datetime
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User)
    role_alt = models.CharField(max_length=256, null=False)

class Vehicles(models.Model):
    id = models.AutoField(primary_key=True)
    driver_user = models.ForeignKey(User, blank=True, null=True, related_name='user_vehicle')
    vehicle = models.CharField(max_length=256, blank=True)
    license_plate = models.CharField(max_length=64, blank=True)
    enabled = models.BooleanField(default=1)
    busy = models.BooleanField(default=0)
    create_time =models.DateTimeField(default=timezone.now, editable=False, blank=True, null=True)

class Rides(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicles, blank=True, null=True, related_name='drive_rides')
    client_user = models.ForeignKey(User, blank=True, null=True, related_name='client_rides')
    origin = models.CharField(max_length=256, blank=True)
    destiny = models.CharField(max_length=512, blank=True)
    status = models.CharField(max_length=64, blank=True)
    create_time =models.DateTimeField(default=timezone.now, editable=False, blank=True, null=True)
    
 