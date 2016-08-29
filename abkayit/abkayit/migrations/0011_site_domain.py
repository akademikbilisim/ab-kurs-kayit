# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0010_site_needs_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='domain',
            field=models.CharField(help_text='To parse incoming requests and show correct page', max_length=128, null=True, verbose_name='domain'),
        ),
    ]
