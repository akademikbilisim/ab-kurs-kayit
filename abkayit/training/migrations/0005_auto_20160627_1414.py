# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0004_auto_20160627_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainesscourserecord',
            name='createdby',
            field=models.ForeignKey(related_name='createdby', default=4, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainesscourserecord',
            name='createtimestamp',
            field=models.DateField(default=django.utils.timezone.now, null=True, verbose_name=b'Creation Timestamp', blank=True),
        ),
        migrations.AddField(
            model_name='trainesscourserecord',
            name='modifiedby',
            field=models.ForeignKey(related_name='modifiedby', default=4, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainesscourserecord',
            name='modifytimestamp',
            field=models.DateField(default=django.utils.timezone.now, null=True, verbose_name=b'Modification Timestamp', blank=True),
        ),
    ]
