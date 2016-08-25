from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone

from abkayit.models import Site
from training.models import Course
from userprofile.models import UserProfile


class Survey(models.Model):
    site = models.ForeignKey(Site, related_name="surveys")
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return u"#{} {}".format(self.id, self.site.name)


class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name="questions")
    key = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    extra = models.TextField(blank=True, default="")
    related_course = models.ForeignKey(Course, blank=True, null=True, related_name="related_questions")
    related_trainer = models.ForeignKey(UserProfile, blank=True, null=True, related_name="related_questions")

    class Meta:
        ordering = ("id",)
        unique_together = [('key', 'survey')]

    def __unicode__(self):
        return u"#{} {}".format(self.id, truncatechars(self.text, 20))


class AnswerGroup(models.Model):
    token = models.CharField(max_length=10, unique=True)
    created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return u"#{} {}".format(self.id, self.token)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers")
    group = models.ForeignKey(AnswerGroup, related_name="answers")
    text = models.TextField(blank=True, default="")

    def __unicode__(self):
        return u"#{} {} ({})".format(self.id, truncatechars(self.text, 20), self.question)

    class Meta:
        ordering = ("id",)
