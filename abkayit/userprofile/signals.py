# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import signals
from abkayit.adaptor import send_email
from abkayit.models import Site
from abkayit.settings import EMAIL_FROM_ADDRESS
from abkayit.backend import create_verification_link
from userprofile.models import UserVerification
import random, hashlib


def send_confirm_link(sender, instance, created, **kwargs):
    if not instance.is_staff:
        if created:
            instance.is_active=False
            user_verification, created = UserVerification.objects.get_or_create(user_email=instance.username)
            user_verification.activation_key = create_verification_link(instance)
            user_verification.save()
            context={}
            context['user'] = instance
            context['activation_key'] = user_verification.activation_key
            domain = Site.objects.get(is_active=True).home_url
            if domain.endswith('/'):
                 domain = domain.rstrip('/')
            context['domain'] = domain
            try:
                 send_email("userprofile/messages/send_confirm_subject.html",
                        "userprofile/messages/send_confirm.html",
                        "userprofile/messages/send_confirm.text",
                        context,
                        EMAIL_FROM_ADDRESS,
                        [instance.username])
            except:
                 raise Exception(_("Your account has been created but has been failed send email verification link"))
    


signals.post_save.connect(send_confirm_link, sender=User)
