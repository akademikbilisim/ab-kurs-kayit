# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0005_auto_20160629_2334'),
        ('training', '0007_auto_20160628_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainessTestAnswers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ManyToManyField(to='abkayit.Answer')),
                ('tcourserecord', models.ForeignKey(to='training.TrainessCourseRecord')),
            ],
            options={
                'verbose_name': 'Trainess Test Answer',
                'verbose_name_plural': 'Trainess Test Answer',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='question',
            field=models.ManyToManyField(to='abkayit.Question', blank=True),
        ),
    ]
