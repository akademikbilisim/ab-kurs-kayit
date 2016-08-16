# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0006_textboxquestions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='detail',
            field=models.CharField(max_length=500, verbose_name='Detail'),
        ),
        migrations.AlterField(
            model_name='content',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Content Name'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='question',
            name='detail',
            field=models.CharField(max_length=5000, verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='site',
            name='home_url',
            field=models.CharField(max_length=128, null=True, verbose_name='Home Url'),
        ),
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Site Name'),
        ),
        migrations.AlterField(
            model_name='site',
            name='year',
            field=models.CharField(max_length=4, verbose_name='Year'),
        ),
    ]
