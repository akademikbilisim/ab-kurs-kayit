#!/usr/bin/env python
#!-*- coding:utf-8 -*-

from django.contrib.auth.models import User
from userprofile.models import UserProfile,UserAccomodationPref
from training.models import Course, TrainessCourseRecord

from django.db.models import Count
def sayilar():
    countO=TrainessCourseRecord.objects.filter(approved=True)
    print "Onaylananlarin sayisi",len(countO)
    countT=TrainessCourseRecord.objects.filter(trainess_approved=True)
    print "Teyit edenlerin sayisi",len(countT)
    for ct in countT:
        ctas=UserAccomodationPref.objects.filter(user=ct.trainess)
        for cta in ctas:
            print cta.user,";",cta.accomodation,";",cta.preference_order
