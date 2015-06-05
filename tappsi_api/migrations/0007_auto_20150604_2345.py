# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tappsi_api', '0006_auto_20150604_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='active',
            field=models.BooleanField(),
        ),
    ]
