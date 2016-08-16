# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='score',
        ),
        migrations.AlterField(
            model_name='trainessnote',
            name='note',
            field=models.CharField(max_length=500, verbose_name='Note'),
        ),
    ]
