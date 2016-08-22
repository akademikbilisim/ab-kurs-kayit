# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0006_auto_20160627_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainesscourserecord',
            name='approvedby',
        ),
        migrations.RemoveField(
            model_name='trainesscourserecord',
            name='createdby',
        ),
        migrations.RemoveField(
            model_name='trainesscourserecord',
            name='createtimestamp',
        ),
    ]
