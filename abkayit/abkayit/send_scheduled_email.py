#!-*- coding:utf-8 -*-
# !/usr/bin/env python

import os
import sys
import django

reload(sys)


def send_all_consent_email():
    from training.models import TrainessCourseRecord
    from abkayit.backend import send_email_by_operation_name
    from abkayit.models import Site
    active_site = Site.objects.get(is_active=True)
    data = {'site': active_site}
    trainessrecords = TrainessCourseRecord.objects.filter(course__site=active_site, approved=True, consentemailsent=False)
    for trainessrecord in trainessrecords:
        data["recipientlist"] = [trainessrecord.trainess.user.username]
        data["approvedpref"] = trainessrecord
        send_email_by_operation_name(data, "send_consent_email")
        trainessrecord.consentemailsent = True
        trainessrecord.save()


def send_to_not_approved_trainess_email(functionname):
    from training.models import TrainessCourseRecord
    from abkayit.backend import send_email_by_operation_name
    from abkayit.models import Site
    import logging
    log = logging.getLogger(__name__)
    active_site = Site.objects.get(is_active=True)
    data = {'site': active_site}
    trainessrecords = TrainessCourseRecord.objects.filter(course__site=active_site, approved=False,
                                                          consentemailsent=False)
    for trainessrecord in trainessrecords:
        has_approved_pref = TrainessCourseRecord.objects.filter(trainess=trainessrecord.trainess, approved=True,
                                                                course__site=active_site)
        if not has_approved_pref:
            data["recipientlist"] = [trainessrecord.trainess.user.username]
            data["approvedpref"] = trainessrecord
            if send_email_by_operation_name(data, functionname):
                log.info(
                    "%s kullanicisina %s"
                    " maili gonderildi" % (trainessrecord.trainess.user.username, functionname),
                    extra={'clientip': '', 'user': 'nginx'})


if __name__ == "__main__":
    try:
        path = sys.argv[1]
        function = sys.argv[2]
        if path not in sys.path:
            sys.path.append(path)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abkayit.settings")
        django.setup()
        if function == "send_all_consent_email":
            send_all_consent_email()
        elif function in ["not_approved_trainess_after_approval_period_ends", "not_approved_trainess_eventstardate"]:
            send_to_not_approved_trainess_email(function)
    except:
        print "Project path can not be empty!"
