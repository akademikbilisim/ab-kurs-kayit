#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from userprofile.models import UserAccomodationPref
from training.models import TrainessCourseRecord


def sayilar():
    countO = TrainessCourseRecord.objects.filter(approved=True)
    print "Onaylananlarin sayisi", len(countO)
    countT = TrainessCourseRecord.objects.filter(trainess_approved=True)
    print "Teyit edenlerin sayisi", len(countT)
    target = open("son_sayilar", 'w')
    for ct in countO:
        ctas = UserAccomodationPref.objects.filter(user=ct.trainess)
        yazilacak = ct.trainess.user.first_name + ";"
        yazilacak += ct.trainess.user.last_name + ";"
        yazilacak += ct.trainess.user.username + ";"
        yazilacak += (str(ct.trainess.gender) or "") + ";"
        yazilacak += (str(ct.trainess.tckimlikno) or "") + ";"
        yazilacak += (ct.trainess.university or "") + ";"
        yazilacak += (ct.trainess.organization or "") + ";"
        yazilacak += (ct.course.name or "") + ";"
        yazilacak += str(ct.preference_order or "") + ";"
        yazilacak += str(ct.trainess_approved) + ";"
        if len(ctas) > 0:
            for cta in ctas:
                yazilacak += (cta.accomodation.name or "") + ";" + (str(cta.preference_order) or "") + ";"
        else:
            yazilacak += ";"
        target.write(yazilacak.encode("utf-8"))
        target.write("\n")
    target.close()
