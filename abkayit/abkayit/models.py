#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField


def make_choices(choices):
	"""
	Returns tuples of localized choices based on the dict choices parameter.
	Uses lazy translation for choices names.
	"""
	return tuple([(k, _(v)) for k, v in choices.items()])

class Site(models.Model):
	name = models.CharField(verbose_name=_("Site Name"), max_length="255")
	year = models.CharField(verbose_name=_("Year"),max_length="4")
	logo = models.ImageField(verbose_name=_("Logo"),upload_to="static/images/")
	is_active = models.BooleanField(verbose_name=_("Is Active"),default=False)
	def __unicode__(self):
		return self.name


class Menu(models.Model):
	name = models.CharField(verbose_name=_("Name"),max_length="255")
	order = models.IntegerField(verbose_name=_("Order"))
	site = models.ForeignKey(Site)
	def __unicode__(self):
		return self.name
	class Meta:
		unique_together = ('order', 'site',)


class Content(models.Model):
	name = models.CharField(verbose_name=_("Content Name"), max_length="255")
	content = RichTextField(verbose_name=_("HTML Content"))
	menu = models.OneToOneField(Menu, related_name="+", null=True)
	def __unicode__(self):
		return self.name
