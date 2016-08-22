# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import userprofile.models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0010_userprofile_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='document',
            field=models.FileField(upload_to=userprofile.models.user_directory_path, null=True, verbose_name='Belge Ekle', blank=True),
        ),
    ]
