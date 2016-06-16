# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_remove_emailtemplate_body_plain'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailtemplate',
            options={'verbose_name': 'E-posta sablonu', 'verbose_name_plural': 'E-posta sablonlari'},
        ),
    ]
