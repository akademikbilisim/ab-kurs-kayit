#!/usr/bin/env python
#!-*- coding:utf-8 -*-

from django.contrib.auth.models import User
from userprofile.models import UserProfile
from training.models import Course, TrainessCourseRecord

def onayla():
    coursepk = 39 # Kursiyerlerin hangi kurs tercihleri onaylanacak?
    with open("onaylanacaklar") as e: # Burada onaylanacak kisilerin eposta adreslerinin bulundugu dosya gelecek (her satirda bir adres)
        kursiyerler = e.readlines()
        for k in kursiyerler:
            print k
            ku = User.objects.get(username=k.rstrip())
            kup = UserProfile.objects.get(user=ku)
            kupts = TrainessCourseRecord.objects.filter(trainess=kup).filter(course__pk=coursepk)
            for kupt in kupts:
               print kupt.trainess.user.username
               kupt.approved=True
               kupt.save()
               print kupt.approved
