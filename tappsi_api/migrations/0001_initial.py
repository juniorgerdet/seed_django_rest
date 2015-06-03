# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role_alt', models.CharField(max_length=256)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rides',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('origin', models.CharField(max_length=256, blank=True)),
                ('destiny', models.CharField(max_length=512, blank=True)),
                ('status', models.CharField(max_length=64, blank=True)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, null=True, editable=False, blank=True)),
                ('client_user', models.ForeignKey(related_name=b'client_rides', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
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
            name='vehicle',
            field=models.ForeignKey(related_name=b'drive_rides', blank=True, to='tappsi_api.Vehicles', null=True),
            preserve_default=True,
        ),
    ]
