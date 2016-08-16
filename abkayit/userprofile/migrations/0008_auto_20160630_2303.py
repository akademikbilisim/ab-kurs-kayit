# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_auto_20160630_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='additional_information',
            field=models.TextField(null=True, verbose_name='Additional Information', blank=True),
        ),
        migrations.AlterField(
            model_name='userverification',
            name='activation_key_expires',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userverification',
            name='password_reset_key',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userverification',
            name='password_reset_key_expires',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
