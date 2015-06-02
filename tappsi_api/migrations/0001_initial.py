# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rides',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('origin', models.CharField(max_length=256, blank=True)),
                ('destiny', models.CharField(max_length=512, blank=True)),
                ('vehicle', models.CharField(max_length=512, blank=True)),
                ('status', models.CharField(max_length=64, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfiles',
            fields=[
                ('user', models.ForeignKey(related_name=b'profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(max_length=1, null=True, blank=True)),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('role_alt', models.CharField(max_length=256, null=True, blank=True)),
                ('profile_pic', models.CharField(max_length=500, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vehicles',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('vehicle', models.CharField(max_length=256, blank=True)),
                ('license_plate', models.CharField(max_length=64, blank=True)),
                ('enabled', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, null=True, editable=False, blank=True)),
                ('driver_user', models.ForeignKey(related_name=b'user_vehicle', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rides',
            name='client_user',
            field=models.ForeignKey(related_name=b'client_rides', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rides',
            name='driver_user',
            field=models.ForeignKey(related_name=b'drive_rides', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
