# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tappsi_api', '0003_auto_20150603_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicles',
            name='driver_user',
        ),
        migrations.RenameField(
            model_name='rides',
            old_name='client_user',
            new_name='client',
        ),
        migrations.RemoveField(
            model_name='rides',
            name='vehicle',
        ),
        migrations.DeleteModel(
            name='Vehicles',
        ),
        migrations.AddField(
            model_name='rides',
            name='taxi_drive',
            field=models.ForeignKey(related_name=b'drive_rides', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
