#!-*- coding-utf8 -*-
# coding=utf-8

from django import template

from userprofile.models import TrainessClassicTestAnswers

register = template.Library()


@register.simple_tag(name="getanswer")
def getanswer(question, user):
    try:
        return TrainessClassicTestAnswers.objects.get(question=question, user=user.userprofile).answer
    except:
        return ""
