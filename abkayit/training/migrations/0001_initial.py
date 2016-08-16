# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0001_initial'),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('no', models.CharField(max_length=b'4', verbose_name='Course No')),
                ('name', models.CharField(max_length=b'255', verbose_name='Course Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('approved', models.BooleanField(default=False)),
                ('application_is_open', models.BooleanField(default=True)),
                ('url', models.CharField(max_length=b'350', verbose_name='URL')),
                ('site', models.ForeignKey(to='abkayit.Site')),
                ('trainer', models.ManyToManyField(related_name='trainer', to='userprofile.UserProfile')),
                ('trainess', models.ManyToManyField(related_name='trainess', to='userprofile.UserProfile', blank=True)),
            ],
            options={
                'verbose_name': 'Kurs',
                'verbose_name_plural': 'Kurslar',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=b'64', verbose_name='Anahtar Kelimeler')),
            ],
        ),
        migrations.CreateModel(
            name='TrainessCourseRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('preference_order', models.SmallIntegerField(default=1)),
                ('approved', models.BooleanField(default=False)),
                ('trainess_approved', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='training.Course')),
                ('trainess', models.ForeignKey(to='userprofile.UserProfile')),
            ],
            options={
                'verbose_name': 'Kursiyer Kurs Tercihi',
                'verbose_name_plural': 'Kursiyer Kurs Tercihleri',
            },
        ),
    ]
