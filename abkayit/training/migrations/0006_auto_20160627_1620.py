# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0005_auto_20160627_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainesscourserecord',
            name='modifiedby',
        ),
        migrations.RemoveField(
            model_name='trainesscourserecord',
            name='modifytimestamp',
        ),
        migrations.AddField(
            model_name='trainesscourserecord',
            name='approvedby',
            field=models.ForeignKey(related_name='approvedby', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='trainesscourserecord',
            name='createdby',
            field=models.ForeignKey(related_name='createdby', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
