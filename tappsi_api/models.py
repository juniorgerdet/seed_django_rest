from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta, datetime
from django.utils import timezone

class UserProfiles(models.Model):
    user = models.ForeignKey(User, primary_key=True, related_name='profile')
    gender = models.CharField(max_length=1, blank=True, null=True)
    birthdate = models.DateField(auto_now=False, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    role_alt = models.CharField(max_length=256, blank=False, null=False)
    profile_pic = models.CharField(max_length=500, blank=True, null=True)

# class Drivers(models.Model):
# 	license = 

class Vehicles(models.Model):
    id = models.AutoField(primary_key=True)
    driver_user = models.ForeignKey(User, blank=True, null=True, related_name='user_vehicle')
    vehicle = models.CharField(max_length=256, blank=True)
    license_plate = models.CharField(max_length=64, blank=True)
    enabled = models.BooleanField(default=0)
    create_time =models.DateTimeField(default=timezone.now, editable=False, blank=True, null=True)

class Rides(models.Model):
    id = models.AutoField(primary_key=True)
    driver_user = models.ForeignKey(User, blank=True, null=True, related_name='drive_rides')
    origin = models.CharField(max_length=256, blank=True)
    destiny = models.CharField(max_length=512, blank=True)
    client_user = models.ForeignKey(User, blank=True, null=True, related_name='client_rides')
    vehicle = models.CharField(max_length=512, blank=True)
    status = models.CharField(max_length=64, blank=True)
 