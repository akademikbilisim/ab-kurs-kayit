# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_auto_20160608_1613'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trainessparticipation',
            options={'verbose_name': 'Yoklama Bilgisi', 'verbose_name_plural': 'Yoklama Bilgileri'},
        ),
        migrations.AddField(
            model_name='trainesscourserecord',
            name='consentemailsent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='trainesscourserecord',
            name='instapprovedate',
            field=models.DateField(default=django.utils.timezone.now, null=True, blank=True),
        ),
    ]
