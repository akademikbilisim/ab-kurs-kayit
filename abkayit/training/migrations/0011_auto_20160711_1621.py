# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0010_auto_20160703_2139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trainesscourserecord',
            options={'ordering': ['trainess', 'preference_order'], 'verbose_name': 'Trainess Course Record', 'verbose_name_plural': 'Trainess Course Records'},
        ),
    ]
