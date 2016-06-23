# -*- coding: utf-8 -*-

import logging

from django.db.models import signals
from abkayit.models import Site, ApprovalDate
from training.tutils import define_consentmailtotrainess_cronjob

log = logging.getLogger(__name__)


def definecronjob_signal(instance, created, **kwargs):
    allapprovedates = ApprovalDate.objects.filter(for_instructor=True).order_by('-end_date')
    if allapprovedates:
        define_consentmailtotrainess_cronjob(allapprovedates[0])
        log.info("consentmailtotrainess_cronjob defined for date %s" % allapprovedates[0].end_date.strftime(
            "%Y-%m-%d %H:%M:%S"), extra={'clientip': '', 'user': ''})


signals.post_save.connect(definecronjob_signal, sender=Site)
