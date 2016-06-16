# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_emailtemplate_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='body_html',
            field=models.TextField(max_length=2000, verbose_name=b'HTML E-posta Govdesi'),
        ),
    ]
