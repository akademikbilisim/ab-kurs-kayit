# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('abkayit', '0011_site_domain'),
        ('training', '0013_auto_20160815_1457'),
        ('userprofile', '0019_auto_20160823_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default=b'', blank=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='AnswerGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(unique=True, max_length=10)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=255)),
                ('extra', models.TextField(default=b'', blank=True)),
                ('related_course', models.ForeignKey(related_name='related_questions', blank=True, to='training.Course', null=True)),
                ('related_trainer', models.ForeignKey(related_name='related_questions', blank=True, to='userprofile.UserProfile', null=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('site', models.ForeignKey(related_name='surveys', to='abkayit.Site')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(related_name='questions', to='surman.Survey'),
        ),
        migrations.AddField(
            model_name='answer',
            name='group',
            field=models.ForeignKey(related_name='answers', to='surman.AnswerGroup'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='surman.Question'),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([('key', 'survey')]),
        ),
    ]
