# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0017_instructorinformation_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='current_education',
            field=models.CharField(default='none', max_length=4, verbose_name='Current Education', choices=[(b'orta', 'Middle School'), (b'lise', 'High School'), (b'univ', 'University'), (b'yksk', 'Master'), (b'dktr', 'Doctorate'), (b'none', 'Not a Student')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='occupation',
            field=models.CharField(default='none', max_length=4, verbose_name='Occupation', choices=[(b'kamu', 'Public'), (b'ozel', 'Private'), (b'akdm', 'Academic'), (b'none', 'Unoccupied')]),
            preserve_default=False,
        ),
    ]
