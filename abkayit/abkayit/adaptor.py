# -*- coding: utf-8 -*-

import logging

from crontab import CronTab

from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
from django.template import Context, Template
log = logging.getLogger(__name__)


def send_email(subject_template, content_template, data, from_email, to_addresses):
    try:
        subject_template_instance = Template(subject_template)
        content_template_instace = Template(content_template)
        subject = subject_template_instance.render(Context(data))
        html_content = content_template_instace.render(Context(data))
        msg = EmailMessage(subject, html_content, from_email, to_addresses)
        msg.content_subtype = "html"
        msg.send()
    except Exception as e:
        log.error(e.message, extra={'clientip': '', 'user': ''})
        raise Exception(_("Mail could not be sent"))


def deleteoldjobs(command):
    consentmailtab = CronTab(user=True)
    old_jobs = consentmailtab.find_command(command)
    if len(list(old_jobs)) > 0:
        consentmailtab.remove_all(command=command)
    consentmailtab.write_to_user()


def define_crontab(command, period):
    consentmailtab = CronTab(user=True)
    consentmailjob = consentmailtab.new(command=command)
    consentmailjob.setall(period)
    consentmailjob.enable()
    consentmailtab.write_to_user()
