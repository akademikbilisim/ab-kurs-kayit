# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import userprofile.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('abkayit', '0010_site_needs_document'),
        ('userprofile', '0018_auto_20160815_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileBySite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.FileField(upload_to=userprofile.models.user_directory_path, null=True, verbose_name='Belge Ekle', blank=True)),
                ('needs_document', models.BooleanField(default=False, verbose_name='Needs Document')),
                ('userpassedtest', models.BooleanField(default=False, verbose_name='FAQ is answered?')),
                ('additional_information', models.TextField(null=True, verbose_name='Additional Information', blank=True)),
                ('canapply', models.BooleanField(default=False, verbose_name='Can Apply?')),
                ('potentialinstructor', models.BooleanField(default=False, verbose_name='Potential Instructor')),
                ('site', models.ForeignKey(to='abkayit.Site')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('user__username',),
                'verbose_name': 'User Profile By Site',
                'verbose_name_plural': 'User Profiles By Sites',
            },
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='additional_information',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='document',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='needs_document',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='userpassedtest',
        ),
    ]
