# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0011_auto_20160701_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainessclassictestanswers',
            name='answer',
            field=models.CharField(max_length=2000, verbose_name=b'Cevap'),
        ),
    ]
