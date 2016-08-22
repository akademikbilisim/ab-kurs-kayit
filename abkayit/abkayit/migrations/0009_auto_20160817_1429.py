# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0008_site_docs_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='afternoon',
            field=models.FloatField(default=3.5, verbose_name='Total course hours at afternoon for one day'),
        ),
        migrations.AddField(
            model_name='site',
            name='evening',
            field=models.FloatField(default=2.5, verbose_name='Total course hours at evening for one day'),
        ),
        migrations.AddField(
            model_name='site',
            name='morning',
            field=models.FloatField(default=3.0, verbose_name='Total course hours at morning for one day'),
        ),
    ]
