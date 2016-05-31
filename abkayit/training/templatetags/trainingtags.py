#!-*- coding-utf8 -*-
from datetime import datetime
from django import template

register = template.Library()


@register.simple_tag(name="mod")
def mod(num):
    return -num


@register.simple_tag(name="isdategtnow_head")
def isdategtnow_head(datedict, key):
    now = datetime.now()
    adate = datedict.get(key)
    if adate:
        if adate.end_date > now:
            return "Onayla"
        else:
            return "Gelecegini Teyit Etti"
    return ""


@register.simple_tag(name="isdategtnow_body")
def isdategtnow_body(datedict, key, t, course):
    now = datetime.now()
    adate = datedict.get(key)
    if adate:
        if adate.end_date > now:
            dom = "<div class=\"checkbox\">"
            if t.approved:
                dom += "<input type=\"checkbox\" checked name=\"students%s\" value=\"%s\"/>" % (course.id, t.pk)
            else:
                dom += "<input type=\"checkbox\" name=\"students%s\" value=\"%s\"/>" % (course.id, t.pk)
            dom += "</div>"
            return dom
        else:
            if t.trainess_approved:
                return "Evet"
            else:
                return "Hayir"
    return ""
