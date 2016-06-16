# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0003_auto_20160607_1101'),
        ('mailing', '0003_auto_20160615_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplate',
            name='site',
            field=models.ForeignKey(default=1, to='abkayit.Site'),
            preserve_default=False,
        ),
    ]
