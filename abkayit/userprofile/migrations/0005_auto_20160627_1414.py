# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0004_auto_20160627_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userverification',
            name='user_email',
        ),
        migrations.AddField(
            model_name='userverification',
            name='user',
            field=models.ForeignKey(default=4, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
