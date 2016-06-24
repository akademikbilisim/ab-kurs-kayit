# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import signals

from abkayit.adaptor import send_email, define_consentmailtab, deleteoldjobs
from abkayit.models import Site, ApprovalDate
from abkayit.settings import EMAIL_FROM_ADDRESS, PROJECT_HOME_DIR, VIRTUAL_ENV_PATH
from abkayit.backend import create_verification_link, send_email_by_operation_name
from userprofile.models import UserVerification

from mailing.models import EmailTemplate

from training.tutils import daterange

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


def definecronjob_signal(instance, created, **kwargs):
    '''
        Kabul e-postalarının onaylama tarihi bitiminde  e-postası gönderilmemis kullanicilara e-posta gonderilebilmesi icin
         cronjob tanimi eklenecek
        :param courseid: hangi kurs i
        :return:
    '''
    allapprovedates = ApprovalDate.objects.filter(site=instance, for_instructor=True).order_by('-end_date')
    if allapprovedates:
        eventstartdate = instance.event_start_date
        date_list = daterange(datetime.date(allapprovedates[0].end_date), eventstartdate)
        consentmailcommand = "cd %s && bash_scripts/consentmailtotrainess_cronjob.sh -w %s -pv %s" % (
        PROJECT_HOME_DIR, PROJECT_HOME_DIR, VIRTUAL_ENV_PATH)
        deleteoldjobs(consentmailcommand)
        for d in date_list:
            define_consentmailtab(consentmailcommand, d)
            log.info("consentmailtotrainess_cronjob defined for date %s" % d.strftime(
                "%Y-%m-%d %H:%M:%S"), extra={'clientip': '', 'user': ''})


signals.post_save.connect(send_confirm_link, sender=User)
signals.post_save.connect(definecronjob_signal, sender=Site)
