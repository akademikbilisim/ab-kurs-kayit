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
    for ct in countO:
        ctas=UserAccomodationPref.objects.filter(user=ct.trainess)
        yazilacak = ct.trainess.user.first_name + ";" 
        yazilacak  += ct.trainess.user.last_name  + ";" 
        yazilacak += ct.trainess.user.username + ";"
        yazilacak += (str(ct.trainess.gender) or "") + ";"
        yazilacak += (ct.trainess.university or "") + ";"
        yazilacak += (ct.trainess.organization or "") + ";"
        yazilacak += (ct.course.name or  "") + ";"
        yazilacak += str(ct.preference_order or  "") + ";"
        yazilacak += str(ct.trainess_approved) + ";"
        if len(ctas)>0:
            for cta in ctas:
                yazilacak += (cta.accomodation.name or "") + ";" + (str(cta.preference_order) or "") + ";"
        else:
            yazilacak += ";"
        print yazilacak
