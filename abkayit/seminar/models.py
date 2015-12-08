#!/usr/bin/env python
#!-*- coding:utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from userprofile.models import UserProfile
from abkayit.models import Site

class SeminarTypes(models.Model):
    typename=models.CharField(max_length=20)
    duration=models.IntegerField()

class Seminar(models.Model):
    speaker=models.ManyToManyField(UserProfile)
    seminartype=models.ForeignKey(SeminarTypes,default=1)
    subject = models.CharField(max_length="255", verbose_name=_("Subject"))
    hall = models.CharField(verbose_name=_("Hall"), max_length="255")
    start_date = models.DateField(verbose_name=_("Seminar Date"),blank=True,null=True)
    end_date = models.DateField(verbose_name=_("Seminar Date"),blank=True,null=True)
    description = models.CharField(verbose_name=_("Brief"), max_length="1000",blank=True,null=True)
    fulltext = models.FileField(upload_to='documents/%Y/%m/%d',blank=True,null=True)
    

