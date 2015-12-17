#!/usr/bin/env python
#!-*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from abkayit.settings import USER_TYPES
from django_countries.fields import CountryField
from django_countries.data import COUNTRIES

class UserVerification(models.Model):
	user_email = models.CharField(max_length=40) 
	activation_key = models.CharField(max_length=40, null=True)
	password_reset_key = models.CharField(max_length=40, null=True)
	activation_key_expires = models.DateTimeField(null=True)
	password_reset_key_expires = models.DateTimeField(null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    address = models.TextField(verbose_name=_("Home Address"))
    job = models.CharField(verbose_name=_("Job"),max_length=40)
    city = models.CharField(verbose_name= _("City"),max_length=40)
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
    
class Accommodation(models.Model):
    gender=models.CharField(choices=[('E', 'Erkek'), ('K', 'Kadin')], verbose_name=_("Gender"), max_length=1)
    name=models.CharField(verbose_name=_("Name"), max_length=100)
    address=models.CharField(verbose_name=_("Address"), max_length=300)
    website=models.CharField(verbose_name=_("Website"), max_length=300)
    def __unicode__(self):
        return self.name
    class Meta:
            verbose_name = 'Konaklama Yeri'
            verbose_name_plural = 'Konaklama Yerleri'
