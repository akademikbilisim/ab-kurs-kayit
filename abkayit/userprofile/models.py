#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django_countries.data import COUNTRIES

from abkayit.settings import USER_TYPES, UNIVERSITIES, GENDER, TRANSPORTATION

from abkayit.models import Site


class UserVerification(models.Model):
    user_email = models.CharField(max_length=40)
    activation_key = models.CharField(max_length=40, null=True)
    password_reset_key = models.CharField(max_length=40, null=True)
    activation_key_expires = models.DateTimeField(null=True)
    password_reset_key_expires = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.user_email


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthdate = models.DateField(verbose_name=_("Bird Date"), default=datetime.date(1970, 1, 1))
    tckimlikno = models.CharField(verbose_name=_("Turkish ID No"), max_length=11, blank=True)
    ykimlikno = models.CharField(verbose_name=_("Foreigner ID No"), max_length=11, blank=True)
    gender = models.CharField(choices={'E': _("Male"), 'K': _("Female")}.items(), verbose_name=_("Gender"),
                              max_length=1)
    mobilephonenumber = models.CharField(verbose_name=_("Mobile Phone Number"), max_length=14)
    address = models.TextField(verbose_name=_("Home Address"))
    job = models.CharField(verbose_name=_("Job"), max_length=40)
    city = models.CharField(verbose_name=_("City"), max_length=40)
    country = CountryField(verbose_name=_("Country"), choices=COUNTRIES, default='TR')
    title = models.CharField(verbose_name=_("Title"), max_length=40)
    organization = models.CharField(verbose_name=_("Organization"), max_length=200)
    university = models.CharField(choices=UNIVERSITIES, verbose_name=_("University"), max_length=300, blank=True)
    department = models.CharField(verbose_name=_("Department"), max_length=50)
    is_instructor = models.BooleanField(verbose_name=_("Is Instructor"), default=False)
    additional_information = models.TextField(verbose_name=_("Additional Information"), null=True)
    userpassedtest = models.BooleanField(verbose_name=_("Basvuru yapabilir mi?"), blank=True, default=False)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ('user__username',)


class TrainessNote(models.Model):
    note = models.CharField(verbose_name=_("Note"), max_length=500)
    note_from_profile = models.ForeignKey(UserProfile, related_name="note_from_profile",
                                          null=True)  # from whom - trainer
    note_to_profile = models.ForeignKey(UserProfile, related_name="note_to_profile")  # to whom - traiess
    note_date = models.DateTimeField(default=datetime.datetime.now)
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return self.note_to_profile.user.username


class SubscribeNotice(models.Model):
    usertype = models.CharField(choices=USER_TYPES.items(), verbose_name=_("User Type"), max_length=4)
    subnotice = models.TextField(verbose_name=_("Subscription Notice"))

    def __unicode__(self):
        return self.usertype


class Accommodation(models.Model):
    gender = models.CharField(choices=GENDER.items(), verbose_name=_("Gender"), max_length=1)
    usertype = models.CharField(choices=USER_TYPES.items(), verbose_name=_("User Type"), max_length=15)
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    address = models.CharField(verbose_name=_("Address"), max_length=300)
    website = models.CharField(verbose_name=_("Website"), max_length=300)
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Accommodation")
        verbose_name_plural = _("Accommodations")


class UserAccomodationPref(models.Model):
    user = models.ForeignKey(UserProfile)
    accomodation = models.ForeignKey(Accommodation)
    usertype = models.CharField(choices=USER_TYPES.items(), verbose_name=_("User Type"), max_length=30)
    preference_order = models.SmallIntegerField(default=1)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.user.username

    class Meta:
        verbose_name = _("Participant Accommodation Preference")
        verbose_name_plural = _("Participant Accommodation Preferences")


class InstructorInformation(models.Model):
    user = models.ForeignKey(UserProfile)
    transportation = models.CharField(choices=TRANSPORTATION.items(), verbose_name=_("Transportation"), max_length=1)
    additional_information = models.CharField(verbose_name=_("Additional Information"), max_length=300, null=True)
    arrival_date = models.DateField(verbose_name=_("Arrival Date"), default=datetime.date.today)
    departure_date = models.DateField(verbose_name=_("Departure Date"), default=datetime.date.today)

    def __unicode__(self):
        return self.user.user.username

    class Meta:
        verbose_name = _("Egitmen Ek Bilgiler")
        verbose_name_plural = _("Egitmen Ek Bilgiler")
