# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0003_auto_20160621_1926'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='approvaldate',
            options={'verbose_name': 'Approval Date', 'verbose_name_plural': 'Approval Dates'},
        ),
    ]
