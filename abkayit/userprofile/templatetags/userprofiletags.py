#!-*- coding-utf8 -*-
# coding=utf-8

from django import template

from abkayit.models import ApprovalDate, Site
from userprofile.models import TrainessClassicTestAnswers
from training.models import Course, TrainessCourseRecord

register = template.Library()


@register.simple_tag(name="getanswer")
def getanswer(question, user):
    try:
        return TrainessClassicTestAnswers.objects.get(question=question, user=user.userprofile).answer
    except:
        return ""


@register.simple_tag(name="getanswers")
def getanswers(tuser, ruser, courseid):
    answers = []
    if ruser.is_staff:
        answers = TrainessClassicTestAnswers.objects.filter(user=tuser, question__site__is_active=True)
    elif courseid:
        course = Course.objects.get(pk=int(courseid))
        questions = course.textboxquestion.all()
        for q in questions:
            answers.append(TrainessClassicTestAnswers.objects.filter(question=q, user=tuser))
        answers.extend(TrainessClassicTestAnswers.objects.filter(user=tuser, question__site__is_active=True,
                                                                 question__is_sitewide=True))

    html = ""
    if answers:
        html = "<dt>Cevaplar:</dt><dd><section><ul>"
        for answer in answers:
            html += "<li> <b>" + answer.question.detail + "</b> <p>" + answer.answer + "</p> </li>"
        html += "</section></ul></dd>"

    return html


@register.simple_tag(name="oldeventprefs")
def oldeventprefs(tuser):
    html = ""
    try:
        sites = Site.objects.filter(is_active=False)

        for site in sites:
            trainessoldprefs = TrainessCourseRecord.objects.filter(trainess=tuser, course__site=site).order_by(
                'preference_order')
            if trainessoldprefs:
                html += "<section><p>" + site.name + " - " + site.year + "</p><ul>"
                for top in trainessoldprefs:
                    if top.approved:
                        html += "<li>" + str(top.preference_order) + ".tercih: " + top.course.name + " (Onaylanmış) </li>"
                    else:
                        html += "<li>" + str(top.preference_order) + ".tercih: " + top.course.name + " </li>"
                html += "</ul></section>"
        if html:
            html = "<h4>Eski Tercihleri: </h4>" + html
    except Exception as e:
        print e.message
    return html
