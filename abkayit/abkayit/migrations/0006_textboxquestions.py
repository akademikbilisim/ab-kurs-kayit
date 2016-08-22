# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0005_auto_20160629_2334'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextBoxQuestions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questionno', models.IntegerField()),
                ('detail', models.CharField(max_length=700, verbose_name='Classic Questions')),
                ('active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('is_sitewide', models.BooleanField(default=False, verbose_name='Site Wide')),
                ('site', models.ForeignKey(to='abkayit.Site')),
            ],
            options={
                'verbose_name': 'Classic Question',
                'verbose_name_plural': 'Classic Questions',
            },
        ),
    ]
