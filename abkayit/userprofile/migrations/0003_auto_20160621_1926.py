# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20160608_1613'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trainessnote',
            options={'verbose_name': 'Trainess Note', 'verbose_name_plural': 'Trainess Notes'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ('user__username',), 'verbose_name': 'User Profile', 'verbose_name_plural': 'User Profiles'},
        ),
        migrations.AlterModelOptions(
            name='userverification',
            options={'verbose_name': 'User Verification', 'verbose_name_plural': 'User Verifications'},
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_participant',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_speaker',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_student',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='can_elect',
            field=models.BooleanField(default=False, verbose_name='Can Elect'),
        ),
    ]
