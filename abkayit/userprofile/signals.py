# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.models import User
from django.db.models import signals

from abkayit.adaptor import send_email
from abkayit.models import Site
from abkayit.settings import EMAIL_FROM_ADDRESS
from abkayit.backend import create_verification_link, send_email_by_operation_name
from userprofile.models import UserVerification
from mailing.models import EmailTemplate 
log = logging.getLogger(__name__)


def send_confirm_link(instance, created, **kwargs):
    if not instance.is_staff:
        if created:
            instance.is_active = False
            user_verification, created = UserVerification.objects.get_or_create(user_email=instance.username)
            user_verification.activation_key = create_verification_link(instance)
            user_verification.save()
            context = {'user': instance, 'activation_key': user_verification.activation_key,
                       'site': Site.objects.get(is_active=True), 'recipientlist': [instance.username]}
            context['domain'] = context['site'].home_url.rstrip('/')
            send_email_by_operation_name(context, "send_activation_key")


signals.post_save.connect(send_confirm_link, sender=User)
