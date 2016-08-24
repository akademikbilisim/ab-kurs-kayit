#!-*- coding-utf8 -*-
# coding=utf-8

import logging

from django import template

from abkayit.models import Site

from userprofile.models import TrainessClassicTestAnswers, InstructorInformation
from userprofile.userprofileops import UserProfileOPS

from training.models import Course, TrainessCourseRecord

log = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag(name="getanswer")
def getanswer(question, user):
    try:
        return TrainessClassicTestAnswers.objects.get(question=question, user=user.userprofile).answer
    except:
        return ""


@register.simple_tag(name="getanswers", takes_context=True)
def getanswers(context, tuser, ruser, courseid):
    try:
        answers = []
        if ruser.is_staff:
            answers = TrainessClassicTestAnswers.objects.filter(user=tuser, question__site=context["request"].site)
        elif courseid:
            course = Course.objects.get(pk=int(courseid))
            questions = course.textboxquestion.all()
            for q in questions:
                answers.append(TrainessClassicTestAnswers.objects.get(question=q, user=tuser))
            answers.extend(TrainessClassicTestAnswers.objects.filter(user=tuser, question__site=context["request"].site,
                                                                     question__is_sitewide=True))

        html = ""
        if answers:
            html = "<dt>Cevaplar:</dt><dd><section><ul>"
            for answer in answers:
                html += "<li> <b>" + answer.question.detail + "</b> <p>" + answer.answer + "</p> </li>"
            html += "</section></ul></dd>"

        return html
    except Exception as e:
        log.error(e.message, extra={'clientip': '', 'user': ruser})
        return ""


@register.simple_tag(name="oldeventprefs")
def oldeventprefs(context, tuser):
    html = ""
    try:
        sites = context['request'].site

        for site in sites:
            trainessoldprefs = TrainessCourseRecord.objects.filter(trainess=tuser, course__site=site).order_by(
                    'preference_order')
            if trainessoldprefs:
                html += "<section><p>" + site.name + " - " + site.year + "</p><ul>"
                for top in trainessoldprefs:
                    if top.approved:
                        html += "<li>" + str(
                                top.preference_order) + ".tercih: " + top.course.name + " (Onaylanmış) </li>"
                    else:
                        html += "<li>" + str(top.preference_order) + ".tercih: " + top.course.name + " </li>"
                html += "</ul></section>"
        if html:
            html = "<h4>Eski Tercihleri: </h4>" + html
    except Exception as e:
        log.error(e.message, extra={'clientip': '', 'user': ''})
    return html


@register.simple_tag(name="getoperationsmenu")
def getoperationsmenu(uprofile):
    html = ""

    if UserProfileOPS.is_instructor(uprofile):
        html += """
        <li>
            <a href="/survey/answers/"><i class="fa fa-file-text-o fa-fw"></i> Anket Sonuçları</a>
        </li>
        <li>
        <a href="/egitim/controlpanel"><i class="fa fa-book fa-fw"></i> Kursum</a>
        </li>
        <li>
            <a href="/egitim/katilimciekle"><i class="fa fa-book fa-fw"></i> Kursiyer Ekle</a>
        </li>
        """
    else:
        html += """
        <li>
            <a href="/egitim/applytocourse"><i class="fa fa-check-square-o fa-fw"></i> Kurs Başvurusu</a>
        </li>
        <li>
            <a href="/egitim/approve_course_preference"><i class="fa fa-thumbs-o-up fa-fw"></i> Başvuru Durum/Onayla</a>
        </li>
        """

    return html


@register.simple_tag(name="instinfo")
def instinfo(uprofile):
    html = ""
    if UserProfileOPS.is_instructor(uprofile):
        html += "<li><a href=\"/accounts/egitmen/bilgi\"><i class=\"fa fa-info-circle fa-fw\"></i> Egitmen Bilgileri </a></li>"

    return html


@register.simple_tag(name="getinstinfo")
def getinstinfo(uprofile, site):
    html = ""
    if UserProfileOPS.is_instructor(uprofile):
        try:
            inst_info = InstructorInformation.objects.get(user=uprofile, site=site)
            html = "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (
                inst_info.transportation, inst_info.arrival_date, inst_info.departure_date,
                inst_info.additional_information)
        except Exception as e:
            return "<td></td><td></td><td></td><td></td>"
    return html
