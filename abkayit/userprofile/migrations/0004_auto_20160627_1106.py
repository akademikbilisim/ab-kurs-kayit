# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20160621_1926'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SubscribeNotice',
        ),
        migrations.AlterModelOptions(
            name='instructorinformation',
            options={'verbose_name': 'Instructor Additional Information', 'verbose_name_plural': 'Instructor Additional Information'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(default=datetime.date(1970, 1, 1), verbose_name='Birth Date'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tckimlikno',
            field=models.CharField(max_length=11, verbose_name='TC Identity Number', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='userpassedtest',
            field=models.BooleanField(default=False, verbose_name='Can Apply'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ykimlikno',
            field=models.CharField(max_length=11, verbose_name='Foreign Identity Number', blank=True),
        ),
    ]
