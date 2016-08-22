# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0014_auto_20160723_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=40, verbose_name='Current City'),
        ),
    ]
