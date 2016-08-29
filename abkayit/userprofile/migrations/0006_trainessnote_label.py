# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20160627_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainessnote',
            name='label',
            field=models.CharField(default='sistem', max_length=50, verbose_name='Label'),
            preserve_default=False,
        ),
    ]
