#!/usr/bin/env python
#!-*- coding:utf-8 -*-

from django.contrib.auth.models import User
from userprofile.models import UserProfile
from training.models import Course
from abkayit.models import Site

# delimiter: |
# user model fields: first_name, last_name, email = username 

def savetrainers():
    with open("egitmenler") as e:
        egitmenler = e.readlines()
        for egit in egitmenler:
            cols=egit.split('|')
            egitu = User(first_name=cols[0],last_name=cols[1],email=cols[2],username=cols[2])
            egitu.set_password = '123456'
            egitu.save()
            egitup = UserProfile(user=egitu,
                                 organization=cols[3],
                                 tckimlikno='',
                                 ykimlikno='',
                                 gender='',
                                 mobilephonenumber='',
                                 address='',
                                 job='',
                                 city='',
                                 title='',
                                 university='',
                                 department='',
                                 is_instructor=True) 
            egitup.save()
# no|name|description|url|trainers

def savecourses():
    with open("kurslar") as e:
        kurslar = e.readlines()
        for kurs in kurslar:
            cols=kurs.split('|')
            kursm = Course(no=cols[0],name=cols[1],description=cols[2],approved=True,site=Site.objects.get(is_active=True),url=cols[3])
            kursm.save()
            for egit in cols[4].split(','):
                kursm.trainer.add(UserProfile.objects.get(user__username=egit.rstrip()))
            kursm.save()
