# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tappsi_api', '0005_auto_20150604_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('origin', models.CharField(max_length=256, blank=True)),
                ('destiny', models.CharField(max_length=512, blank=True)),
                ('active', models.BooleanField(default=1)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, null=True, editable=False, blank=True)),
                ('client', models.ForeignKey(related_name=b'client_rides', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('taxi_drive', models.ForeignKey(related_name=b'drive_rides', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='rides',
            name='client',
        ),
        migrations.RemoveField(
            model_name='rides',
            name='taxi_drive',
        ),
        migrations.DeleteModel(
            name='Rides',
        ),
    ]
