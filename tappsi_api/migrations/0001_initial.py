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
            name='Driver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('license_plate', models.CharField(max_length=10, blank=True)),
                ('busy', models.BooleanField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role_alt', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=50, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('origin', models.CharField(max_length=256, blank=True)),
                ('destiny', models.CharField(max_length=512, blank=True)),
                ('active', models.BooleanField(default=1)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, null=True, editable=False, blank=True)),
                ('client', models.ForeignKey(related_name=b'clients', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('taxi_driver', models.ForeignKey(related_name=b'drives', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
