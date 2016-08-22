# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0006_textboxquestions'),
        ('userprofile', '0008_auto_20160630_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainessClassicTestAnswers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=1000, verbose_name=b'Cevap')),
                ('question', models.ForeignKey(verbose_name=b'Soru', to='abkayit.TextBoxQuestions')),
                ('user', models.ForeignKey(to='userprofile.UserProfile')),
            ],
            options={
                'verbose_name': 'Trainess Answer for Classic Question',
                'verbose_name_plural': 'Trainess Answers for Classic Questions ',
            },
        ),
    ]
