#!/usr/bin/env python

# -*- coding:utf-8 -*-

import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django_countries.data import COUNTRIES

from abkayit.settings import USER_TYPES, UNIVERSITIES, GENDER, TRANSPORTATION

from abkayit.models import Site, TextBoxQuestions

OCCUPATIONS = [
    ("kamu", _("Public")),
    ("ozel", _("Private")),
    ("akdm", _("Academic")),
    ("none", _("Unoccupied")),
]

EDUCATIONS = [
    ("orta", _("Middle School")),
    ("lise", _("High School")),
    ("univ", _("University")),
    ("yksk", _("Master")),
    ("dktr", _("Doctorate")),
    ("none", _("Not a Student")),
]


class UserVerification(models.Model):
    user = models.ForeignKey(User)
    activation_key = models.CharField(max_length=40, null=True)
    password_reset_key = models.CharField(max_length=40, null=True, blank=True)
    activation_key_expires = models.DateTimeField(null=True, blank=True)
    password_reset_key_expires = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _('User Verification')
        verbose_name_plural = _('User Verifications')


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthdate = models.DateField(verbose_name=_("Birth Date"), default=datetime.date(1970, 1, 1))
    tckimlikno = models.CharField(verbose_name=_("TC Identity Number"), max_length=11, blank=True)
    ykimlikno = models.CharField(verbose_name=_("Foreign Identity Number"), max_length=11, blank=True)
    gender = models.CharField(choices={'E': _("Male"), 'K': _("Female")}.items(), verbose_name=_("Gender"),
                              max_length=1)
    mobilephonenumber = models.CharField(verbose_name=_("Mobile Phone Number"), max_length=14)
    address = models.TextField(verbose_name=_("Home Address"))
    job = models.CharField(verbose_name=_("Job"), max_length=40, null=True, blank=True)
    city = models.CharField(verbose_name=_("Current City"), max_length=40)
    country = CountryField(verbose_name=_("Nationality"), choices=COUNTRIES, default='TR')
    title = models.CharField(verbose_name=_("Title"), max_length=40)
    occupation = models.CharField(verbose_name=_("Occupation"), choices=OCCUPATIONS, max_length=4)
    current_education = models.CharField(verbose_name=_("Current Education"), choices=EDUCATIONS, max_length=4)
    organization = models.CharField(verbose_name=_("Organization"), max_length=200, null=True, blank=True)
    university = models.CharField(choices=UNIVERSITIES, verbose_name=_("University"), max_length=300, blank=True)
    department = models.CharField(verbose_name=_("Department"), max_length=50)
    website = models.CharField(verbose_name=_("Website"), max_length=300, null=True, blank=True)
    experience = models.CharField(verbose_name=_("Work Experience"), max_length=1000, null=True, blank=True)
    profilephoto = models.ImageField(upload_to=user_directory_path, verbose_name=_("Profile Picture"))

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ('user__username',)
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')


class UserProfileBySite(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site)
    document = models.FileField(upload_to=user_directory_path, verbose_name=_("Belge Ekle"), blank=True, null=True)
    needs_document = models.BooleanField(verbose_name=_("Needs Document"), blank=True, default=False)
    userpassedtest = models.BooleanField(verbose_name=_("FAQ is answered?"), blank=True, default=False)
    additional_information = models.TextField(verbose_name=_("Additional Information"), blank=True, null=True)
    canapply = models.BooleanField(verbose_name=_("Can Apply?"), blank=True, default=False)
    potentialinstructor = models.BooleanField(verbose_name=_("Potential Instructor"), blank=True, default=False)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ('user__username',)
        verbose_name = _('User Profile By Site')
        verbose_name_plural = _('User Profiles By Sites')


class TrainessNote(models.Model):
    note = models.CharField(verbose_name=_("Note"), max_length=500)
    note_from_profile = models.ForeignKey(UserProfile, related_name="note_from_profile",
                                          null=True)  # from whom - trainer
    note_to_profile = models.ForeignKey(UserProfile, related_name="note_to_profile")  # to whom - traiess
    note_date = models.DateTimeField(default=datetime.datetime.now)
    site = models.ForeignKey(Site)
    label = models.CharField(max_length=50, verbose_name=_("Label"))

    def __unicode__(self):
        return self.note_to_profile.user.username

    class Meta:
        verbose_name = _('Trainess Note')
        verbose_name_plural = _('Trainess Notes')


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
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return self.user.user.username

    class Meta:
        verbose_name = _("Instructor Additional Information")
        verbose_name_plural = _("Instructor Additional Information")


class TrainessClassicTestAnswers(models.Model):
    user = models.ForeignKey(UserProfile)
    question = models.ForeignKey(TextBoxQuestions, verbose_name="Soru")
    answer = models.CharField(max_length=2000, verbose_name="Cevap")

    def __unicode__(self):
        return self.user.user.username

    class Meta:
        verbose_name = _("Trainess Answer for Classic Question")
        verbose_name_plural = _("Trainess Answers for Classic Questions ")
