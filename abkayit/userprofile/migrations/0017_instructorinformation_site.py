# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0007_auto_20160815_1457'),
        ('userprofile', '0016_auto_20160815_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructorinformation',
            name='site',
            field=models.ForeignKey(default=2, to='abkayit.Site'),
            preserve_default=False,
        ),
    ]
