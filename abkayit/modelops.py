#!/usr/bin/env python
#!-*- coding:utf-8 -*-

from django.contrib.auth.models import User
from userprofile.models import UserProfile
from training.models import Course
from abkayit.models import Site

# delimiter: |
# user model fields: first_name, last_name, email = username 

def savetrainers():
    with open("sisteme_eklenecek_egitmenler.csv") as e:
        egitmenler = e.readlines()
        for egit in egitmenler:
            print egit
            cols=egit.split('|')
            try:
                egitu = User(first_name=cols[0],last_name=cols[1],email=cols[4].rstrip(),username=cols[4].rstrip())
                egitu.set_password = '123456'
                egitu.save()
                egitup = UserProfile(user=egitu,
                                     organization=cols[2],
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
                                     country=cols[3],
                                     is_instructor=True) 
                egitup.save()
                print "olustu"
                print cols[4].rstrip()
            except:
                print "olusmadi"
                print cols[4].rstrip()
# no|name|description|url|trainers

def savecourses():
    with open("courses") as e:
        kurslar = e.readlines()
        for kurs in kurslar:
            print kurs
            try:
                print "olustu"
                cols=kurs.split('|')
                kursm = Course(no=cols[0],name=cols[1],description='',
                               approved=True, site=Site.objects.get(is_active=True),
                               url="http://ab.org.tr/ab16/kursdir/"+str(cols[0])+".html")
                kursm.save()
                for egit in cols[2].split(','):
                    print egit
                    user=User.objects.get(username=egit.rstrip())
                    kursm.trainer.add(UserProfile.objects.get(user=user))
                kursm.save()
            except:
                print "olusmadi"
