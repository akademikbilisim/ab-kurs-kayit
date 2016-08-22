# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import userprofile.models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_trainessnote_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='experience',
            field=models.CharField(max_length=1000, null=True, verbose_name='Work Experience', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profilephoto',
            field=models.ImageField(default='user/', upload_to=userprofile.models.user_directory_path, verbose_name='Profile Picture'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='website',
            field=models.CharField(max_length=300, null=True, verbose_name='Website', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='job',
            field=models.CharField(max_length=40, null=True, verbose_name='Job', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='organization',
            field=models.CharField(max_length=200, null=True, verbose_name='Organization', blank=True),
        ),
    ]
