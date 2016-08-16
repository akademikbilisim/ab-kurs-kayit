# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0012_course_authorized_trainer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Course Name'),
        ),
        migrations.AlterField(
            model_name='course',
            name='no',
            field=models.CharField(max_length=4, verbose_name='Course No'),
        ),
        migrations.AlterField(
            model_name='course',
            name='url',
            field=models.CharField(max_length=350, verbose_name='URL'),
        ),
    ]
