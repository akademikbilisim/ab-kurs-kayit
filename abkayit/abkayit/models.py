#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

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
    home_url = models.CharField(verbose_name=_("Home Url"), max_length="128", null=True)
    application_start_date = models.DateField(verbose_name=_("Course Application Start Date"), default=datetime.now) 
    application_end_date = models.DateField(verbose_name=_("Course Application End Date"), default=datetime.now) 
    aproval_start_date = models.DateField(verbose_name=_("Trainess Aproval Start Date"), default=datetime.now) 
    aproval_end_date = models.DateField(verbose_name=_("Trainess Aproval End Date"), default=datetime.now) 
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
