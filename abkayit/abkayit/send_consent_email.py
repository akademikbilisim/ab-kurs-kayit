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

if __name__ == "__main__":
    try:
        path = sys.argv[1]
        if path not in sys.path:
            sys.path.append(path)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abkayit.settings")
        django.setup()
        send_all_consent_email()
    except:
        print "Project path can not be empty!"
