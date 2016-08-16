# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0006_textboxquestions'),
        ('training', '0008_auto_20160629_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='textboxquestion',
            field=models.ManyToManyField(to='abkayit.TextBoxQuestions', verbose_name=b'Klasik Sorular', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='question',
            field=models.ManyToManyField(to='abkayit.Question', verbose_name=b'\xc3\x87oktan Se\xc3\xa7meli Sorular', blank=True),
        ),
    ]
