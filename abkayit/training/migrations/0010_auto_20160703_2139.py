# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0009_auto_20160701_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='question',
            field=models.ManyToManyField(to='abkayit.Question', verbose_name='Question', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='textboxquestion',
            field=models.ManyToManyField(to='abkayit.TextBoxQuestions', verbose_name='Text Box Questions', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='trainer',
            field=models.ManyToManyField(related_name='trainer', verbose_name='Trainer', to='userprofile.UserProfile'),
        ),
        migrations.AlterField(
            model_name='course',
            name='trainess',
            field=models.ManyToManyField(related_name='trainess', verbose_name='Trainess', to='userprofile.UserProfile', blank=True),
        ),
    ]
