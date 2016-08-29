# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0009_auto_20160817_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='needs_document',
            field=models.BooleanField(default=True, verbose_name='Site requires document'),
        ),
    ]
