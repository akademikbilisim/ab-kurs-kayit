#!/usr/bin/env python
#!-*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from abkayit.settings import USER_TYPES
from django_countries.fields import CountryField
from django_countries.data import COUNTRIES

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    address = models.TextField(verbose_name=_("Home Address"))
    job = models.CharField(verbose_name=_("Job"),max_length=40)
    city = models.CharField(verbose_name= _("City"),max_length=40)
	# ulke kodu tutulacak sadece
    country = CountryField(verbose_name= _("Country"),choices=COUNTRIES,default='TR')
    title =  models.CharField(verbose_name= _("Title"),max_length=40)
    organization= models.CharField(verbose_name= _("Organization"),max_length=50)
    accommodation_needed = models.BooleanField(verbose_name=_("Accommodation Needed"),default=False)
    is_instructor = models.BooleanField(verbose_name=_("Is Instructor"),default=False)
    is_student = models.BooleanField(verbose_name=_("Is Student"),default=False)
    is_speaker = models.BooleanField(verbose_name=_("Is Speaker"),default=False)
    is_participant = models.BooleanField(verbose_name=_("Is Participant"),default=False)
    def __unicode__(self):
        return self.user.username
    
class SubscribeNotice(models.Model):
    usertype=models.CharField(choices=USER_TYPES.items(), verbose_name=_("User Type"), max_length=4)
    subnotice=models.TextField(verbose_name=_("Subscription Notice"))
    def __unicode__(self):
        return self.usertype
