# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0004_auto_20160627_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='choices',
        ),
        migrations.RemoveField(
            model_name='question',
            name='rightanswer',
        ),
        migrations.AddField(
            model_name='answer',
            name='is_right',
            field=models.BooleanField(default=False, verbose_name='Is Right Answer'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='abkayit.Question', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='is_faq',
            field=models.BooleanField(default=True, verbose_name='Is Frequently Asked Question?'),
        ),
    ]
