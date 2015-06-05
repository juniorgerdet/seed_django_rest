# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tappsi_api', '0004_auto_20150604_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rides',
            name='status',
        ),
        migrations.AddField(
            model_name='rides',
            name='active',
            field=models.BooleanField(default=1),
            preserve_default=True,
        ),
    ]
