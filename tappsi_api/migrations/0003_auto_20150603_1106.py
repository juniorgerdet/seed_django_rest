# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tappsi_api', '0002_vehicles_bugsy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicles',
            old_name='bugsy',
            new_name='busy',
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='enabled',
            field=models.BooleanField(default=1),
        ),
    ]
