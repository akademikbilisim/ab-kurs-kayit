# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0003_auto_20160621_1926'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Keyword',
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Course', 'verbose_name_plural': 'Courses'},
        ),
        migrations.AlterModelOptions(
            name='trainesscourserecord',
            options={'verbose_name': 'Trainess Course Record', 'verbose_name_plural': 'Trainess Course Records'},
        ),
        migrations.AlterModelOptions(
            name='trainessparticipation',
            options={'verbose_name': 'Trainess Participation Information', 'verbose_name_plural': 'Trainess Participation Information'},
        ),
        migrations.AlterField(
            model_name='trainessparticipation',
            name='afternoon',
            field=models.CharField(default=b'0', max_length=3, verbose_name='Afternoon', choices=[(b'-1', b'Kurs Yap\xc4\xb1lmad\xc4\xb1'), (b'0', b'Kat\xc4\xb1lmad\xc4\xb1'), (b'1', b'Yar\xc4\xb1s\xc4\xb1na Kat\xc4\xb1ld\xc4\xb1'), (b'2', b'Kat\xc4\xb1ld\xc4\xb1')]),
        ),
        migrations.AlterField(
            model_name='trainessparticipation',
            name='day',
            field=models.CharField(default=b'1', max_length=20, verbose_name='Day'),
        ),
        migrations.AlterField(
            model_name='trainessparticipation',
            name='evening',
            field=models.CharField(default=b'0', max_length=3, verbose_name='Evening', choices=[(b'-1', b'Kurs Yap\xc4\xb1lmad\xc4\xb1'), (b'0', b'Kat\xc4\xb1lmad\xc4\xb1'), (b'1', b'Yar\xc4\xb1s\xc4\xb1na Kat\xc4\xb1ld\xc4\xb1'), (b'2', b'Kat\xc4\xb1ld\xc4\xb1')]),
        ),
        migrations.AlterField(
            model_name='trainessparticipation',
            name='morning',
            field=models.CharField(default=b'0', max_length=3, verbose_name='Morning', choices=[(b'-1', b'Kurs Yap\xc4\xb1lmad\xc4\xb1'), (b'0', b'Kat\xc4\xb1lmad\xc4\xb1'), (b'1', b'Yar\xc4\xb1s\xc4\xb1na Kat\xc4\xb1ld\xc4\xb1'), (b'2', b'Kat\xc4\xb1ld\xc4\xb1')]),
        ),
    ]
