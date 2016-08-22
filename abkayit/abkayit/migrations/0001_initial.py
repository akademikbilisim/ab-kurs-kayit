# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('detail', models.CharField(max_length=b'500', verbose_name='Detail')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
        migrations.CreateModel(
            name='ApprovalDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Start Date')),
                ('end_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='End Date')),
                ('preference_order', models.SmallIntegerField(verbose_name='Preference')),
                ('for_instructor', models.BooleanField(default=True, verbose_name='For Instructor?')),
                ('for_trainess', models.BooleanField(default=False, verbose_name='For Trainess?')),
            ],
            options={
                'verbose_name': 'Approval Date',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=b'255', verbose_name='Content Name')),
                ('content', ckeditor.fields.RichTextField(verbose_name='HTML Content')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=b'255', verbose_name='Name')),
                ('order', models.IntegerField(verbose_name='Order')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('no', models.IntegerField()),
                ('detail', models.CharField(max_length=b'5000', verbose_name='Question')),
                ('active', models.BooleanField(default=False, verbose_name='Is Active')),
                ('choices', models.ManyToManyField(related_name='choices', to='abkayit.Answer')),
                ('rightanswer', models.ForeignKey(related_name='rightanswer', to='abkayit.Answer')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=b'255', verbose_name='Site Name')),
                ('year', models.CharField(max_length=b'4', verbose_name='Year')),
                ('logo', models.ImageField(upload_to=b'images/', verbose_name='Logo')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Active')),
                ('home_url', models.CharField(max_length=b'128', null=True, verbose_name='Home Url')),
                ('application_start_date', models.DateField(default=datetime.datetime.now, verbose_name='Course Application Start Date')),
                ('application_end_date', models.DateField(default=datetime.datetime.now, verbose_name='Course Application End Date')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='site',
            field=models.ForeignKey(to='abkayit.Site'),
        ),
        migrations.AddField(
            model_name='content',
            name='menu',
            field=models.OneToOneField(related_name='+', null=True, to='abkayit.Menu'),
        ),
        migrations.AddField(
            model_name='approvaldate',
            name='site',
            field=models.ForeignKey(to='abkayit.Site'),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('order', 'site')]),
        ),
    ]
