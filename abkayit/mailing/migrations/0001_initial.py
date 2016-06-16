# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operation_name', models.CharField(unique=True, max_length=200, verbose_name=b'Fonksiyon ismi')),
                ('subject', models.CharField(max_length=300, verbose_name=b'Konu')),
                ('body_html', models.CharField(max_length=2000, verbose_name=b'HTML E-posta Govdesi')),
                ('body_plain', models.CharField(max_length=2000, verbose_name=b'D\xc3\xbcz E-posta Govdesi')),
            ],
        ),
    ]
