# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0007_auto_20160815_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='docs_end_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Docs End Date'),
        ),
    ]
