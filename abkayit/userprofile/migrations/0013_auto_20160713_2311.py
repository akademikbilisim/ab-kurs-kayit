# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0012_auto_20160703_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='can_elect',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_instructor',
        ),
    ]
