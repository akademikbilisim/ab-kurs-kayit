# -*- coding: utf-8 -*-

import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_email(subject_template, content_template, content_text, data, from_email, to_addresses):
    d = {'clientip': '', 'user': ''}
    try:
        subject = render_to_string(subject_template, data).strip()
        html_content = render_to_string(content_template, data).strip()
        text_content = render_to_string(content_text, data).strip()
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_addresses])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        logger.error(e, extra=d)
        raise Exception("Mail gonderilemedi!")
