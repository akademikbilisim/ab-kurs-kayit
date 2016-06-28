#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from django.contrib.auth.models import User

from userprofile.models import UserProfile

from abkayit.models import Site
from abkayit.settings import TRAINESS_PARTICIPATION_STATE


def make_choices(choices):
    return tuple([(k, _(v)) for k, v in choices.items()])


class Course(models.Model):
    no = models.CharField(verbose_name=_("Course No"), max_length="4")
    name = models.CharField(verbose_name=_("Course Name"), max_length="255")
    description = models.TextField(verbose_name=_("Description"))
    trainess = models.ManyToManyField(UserProfile, related_name="trainess", blank=True)
    trainer = models.ManyToManyField(UserProfile, related_name="trainer")
    approved = models.BooleanField(default=False)
    application_is_open = models.BooleanField(default=True)
    site = models.ForeignKey(Site)
    url = models.CharField(verbose_name=_("URL"), max_length="350")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')


class TrainessCourseRecord(models.Model):
    trainess = models.ForeignKey(UserProfile)
    course = models.ForeignKey(Course)
    preference_order = models.SmallIntegerField(default=1)
    approved = models.BooleanField(default=False)
    trainess_approved = models.BooleanField(default=False)
    instapprovedate = models.DateField(default=now, blank=True, null=True)
    consentemailsent = models.BooleanField(default=False)

    def __unicode__(self):
        return self.course.name

    class Meta:
        verbose_name = _('Trainess Course Record')
        verbose_name_plural = _('Trainess Course Records')


class TrainessParticipation(models.Model):
    courserecord = models.ForeignKey(TrainessCourseRecord)
    morning = models.CharField(choices=TRAINESS_PARTICIPATION_STATE, verbose_name=_("Morning"), max_length=3, default='0')
    afternoon = models.CharField(choices=TRAINESS_PARTICIPATION_STATE, verbose_name=_("Afternoon"), max_length=3,
                                 default='0')
    evening = models.CharField(choices=TRAINESS_PARTICIPATION_STATE, verbose_name=_("Evening"), max_length=3, default='0')
    day = models.CharField(verbose_name=_("Day"), max_length=20, default='1')

    def __unicode__(self):
        return self.courserecord.trainess.user.username

    class Meta:
        verbose_name = _('Trainess Participation Information')
        verbose_name_plural = _('Trainess Participation Information')
