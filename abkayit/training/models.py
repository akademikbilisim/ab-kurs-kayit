#!/usr/bin/env python
#!-*- coding:utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from userprofile.models import UserProfile
from abkayit.models import Site
 
def make_choices(choices):
	return tuple([(k, _(v)) for k, v in choices.items()])

class Keyword(models.Model):
	name = models.CharField(verbose_name=_("Anahtar Kelimeler"), max_length="64")
	def __unicode__(self):
		return self.name

class Course(models.Model):
	# TODO(later): simdilik sadece asagidaki alanlara ihtiyacimiz var
	# 	gerisini tum portal yapilirken kullanacagiz
	no = models.CharField(verbose_name=_("Course No"), max_length="4")
	name = models.CharField(verbose_name=_("Course Name"), max_length="255")
	description = models.TextField(verbose_name=_("Description"))
	#keyword = models.ManyToManyField(Keyword, required=False)
	#goal = models.TextField(verbose_name=_("Hedef"))
	#partipation_rules = models.TextField(verbose_name=_("Kursa katilacaklardan beklenenler"))
	trainess = models.ManyToManyField(UserProfile, related_name="trainess", null=True, blank=True)
	trainer = models.ManyToManyField(UserProfile, related_name="trainer")
	approved = models.BooleanField(default=False) 
	application_is_open = models.BooleanField(default=True) 
	site = models.ForeignKey(Site)
        #fulltext = models.FileField(upload_to='documents/%Y/%m/%d',null=True)
	url = models.CharField(verbose_name=_("URL"), max_length="350")
	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name = 'Kurs'
		verbose_name_plural = 'Kurslar'

class TrainessCourseRecord(models.Model):
	trainess = models.ForeignKey(UserProfile)
	course = models.ForeignKey(Course)
	preference_order = models.SmallIntegerField(default=1)
	approved = models.BooleanField(default=False)
	def __unicode__(self):
		return self.course.name
	class Meta:
		verbose_name = 'Kursiyer Kurs Tercihi'
		verbose_name_plural = 'Kursiyer Kurs Tercihleri'
