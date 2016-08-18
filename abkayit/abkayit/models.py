#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField


def make_choices(choices):
    """
    :param choices: Returns tuples of localized choices based on the dict choices parameter.
    Uses lazy translation for choices names.
    """
    return tuple([(k, _(v)) for k, v in choices.items()])


class Site(models.Model):
    name = models.CharField(verbose_name=_("Site Name"), max_length=255)
    year = models.CharField(verbose_name=_("Year"), max_length=4)
    logo = models.ImageField(verbose_name=_("Logo"), upload_to="images/")
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=False)
    home_url = models.CharField(verbose_name=_("Home Url"), max_length=128, null=True)
    domain = models.CharField(verbose_name=_("domain"), max_length=128, null=True,
                              help_text=_("To parse incoming requests and show correct page"))
    application_start_date = models.DateField(verbose_name=_("Course Application Start Date"), default=datetime.now)
    application_end_date = models.DateField(verbose_name=_("Course Application End Date"), default=datetime.now)
    event_start_date = models.DateField(verbose_name=_("Event Start Date"), default=datetime.now)
    event_end_date = models.DateField(verbose_name=_("Event End Date"), default=datetime.now)
    docs_end_date = models.DateField(verbose_name=_("Docs End Date"), default=datetime.now)
    morning = models.FloatField(verbose_name=_("Total course hours at morning for one day"), default=3.0)
    afternoon = models.FloatField(verbose_name=_("Total course hours at afternoon for one day"), default=3.5)
    evening = models.FloatField(verbose_name=_("Total course hours at evening for one day"), default=2.5)
    needs_document = models.BooleanField(verbose_name=_("Site requires document"), default=True)

    def __unicode__(self):
        return "%s %s" % (self.name, self.year)


class Menu(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    order = models.IntegerField(verbose_name=_("Order"))
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('order', 'site',)


class Content(models.Model):
    name = models.CharField(verbose_name=_("Content Name"), max_length=255)
    content = RichTextField(verbose_name=_("HTML Content"))
    menu = models.OneToOneField(Menu, related_name="+", null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Content')
        verbose_name_plural = _('Contents')


class Question(models.Model):
    no = models.IntegerField()
    detail = models.CharField(verbose_name=_("Question"), max_length=5000)
    active = models.BooleanField(verbose_name=_("Is Active"), default=False)
    is_faq = models.BooleanField(verbose_name=_("Is Frequently Asked Question?"), default=True)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __unicode__(self):
        return self.detail


class Answer(models.Model):
    question = models.ForeignKey(Question, null=True)
    detail = models.CharField(verbose_name=_("Detail"), max_length=500)
    is_right = models.BooleanField(verbose_name=_("Is Right Answer"), default=False)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __unicode__(self):
        return self.detail


class TextBoxQuestions(models.Model):
    questionno = models.IntegerField()
    site = models.ForeignKey(Site)
    detail = models.CharField(max_length=700, verbose_name=_("Classic Questions"))
    active = models.BooleanField(verbose_name=_("Is Active"), default=True)
    is_sitewide = models.BooleanField(verbose_name=_("Site Wide"), default=False)

    class Meta:
        verbose_name = _("Classic Question")
        verbose_name_plural = _("Classic Questions")

    def __unicode__(self):
        return self.detail


class ApprovalDate(models.Model):
    start_date = models.DateTimeField(verbose_name=_("Start Date"), default=datetime.now)
    end_date = models.DateTimeField(verbose_name=_("End Date"), default=datetime.now)
    preference_order = models.SmallIntegerField(verbose_name=_("Preference"))
    site = models.ForeignKey(Site)
    for_instructor = models.BooleanField(verbose_name=_("For Instructor?"), default=True)
    for_trainess = models.BooleanField(verbose_name=_("For Trainess?"), default=False)

    def __unicode__(self):
        return self.end_date.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = _("Approval Date")
        verbose_name_plural = _("Approval Dates")
