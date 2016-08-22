# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0002_auto_20160608_1613'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'verbose_name': 'Content', 'verbose_name_plural': 'Contents'},
        ),
    ]
