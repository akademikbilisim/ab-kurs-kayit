#!-*- coding:utf-8 -*-

import hashlib
import logging
import random

from django.core.exceptions import *
from django.utils.translation import ugettext_lazy as _

from abkayit.models import Site, Menu
from abkayit.settings import EMAIL_FROM_ADDRESS
from abkayit.adaptor import send_email

from mailing.models import EmailTemplate

log = logging.getLogger(__name__)


def getsiteandmenus(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    site = None
    menus = []
    try:
        site = Site.objects.get(is_active=True)
        menus = site.menu_set.order_by('order')
    except ObjectDoesNotExist:
        log.error("active site not found" % request.user, extra=d)
    return {'menus': menus, 'site': site, 'user': request.user}


def create_verification_link(user):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    return hashlib.sha1(salt + user.username).hexdigest()


def send_email_by_operation_name(context, operation_name):
    try:
        emailtemplate = EmailTemplate.objects.get(operation_name=operation_name)
        send_email(emailtemplate.subject,
                   emailtemplate.body_html,
                   context,
                   EMAIL_FROM_ADDRESS,
                   context['recipientlist'])
        return 1
    except Exception as e:
        log.error(e.message, extra={'clientip': context.get('clientip', ''), 'user': context.get('user', '')})
        return 0