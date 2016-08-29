# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0013_auto_20160713_2311'),
        ('training', '0011_auto_20160711_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='authorized_trainer',
            field=models.ManyToManyField(related_name='authorized_trainer', verbose_name='Authorized Trainers', to='userprofile.UserProfile'),
        ),
    ]
