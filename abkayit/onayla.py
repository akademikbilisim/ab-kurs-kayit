#!/usr/bin/env python
#!-*- coding:utf-8 -*-
import sys
import os
import django

def onayla():
    from django.contrib.auth.models import User
    from userprofile.models import UserProfile
    from training.models import Course, TrainessCourseRecord
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

def karalisteimport():
    from userprofile.models import UserProfile, TrainessNote
    from abkayit.models import Site
    from datetime import datetime
    #with open("karaliste.csv.bk") as f:
    with open("blacklist_with_3_name") as f:
        blacklisteduser = f.readlines()
        for user in blacklisteduser:
            userfields = user.split(",")
            userobj = None
            if userfields[1] and userfields[1] != "-":
                userobj = UserProfile.objects.filter(tckimlikno=userfields[1])
            if not userobj and userfields[2] and userfields[2] != "-":
                userobj = UserProfile.objects.filter(user__username=userfields[2])
            if userobj:
                site = Site.objects.get(name=userfields[3], year=userfields[4])
                if site:
                    #trainessnote = TrainessNote(site=site, note_to_profile=userobj[0], note_from_profile=UserProfile.objects.get(user__username="ozge@kripton.rocks"), label="sistem", note=userfields[5])
                    #trainessnote.save()
                    #print "*******"
                    #print userfields[0]
                    #print userobj
                    pass
                else:
                    print "******* Profil var site yok"
                    print userfields[0]
                    print userobj
            else:
                name = userfields[0].split(" ")[0] + " " + userfields[0].split(" ")[1]
                surname = userfields[0].split(" ")[2]
                userobj2 = UserProfile.objects.filter(user__first_name=name, user__last_name=surname)
                if userobj2:
                    site = Site.objects.get(name=userfields[3], year=userfields[4])
                    if site:
                    #    trainessnote = TrainessNote(site=site, note_to_profile=userobj2[0], note_from_profile=UserProfile.objects.get(user__username="ozge@kripton.rocks"), label="sistem", note=userfields[5])
                    #    trainessnote.save()
                        print "*******"
                        print userfields[0]
                        print userobj2
                        #pass
                    else:
                        print "******* Profil var site yok"
                        print userfields[0]
                        print userobj2


if __name__ == "__main__":
    #try:
    path = sys.argv[1]
    if path not in sys.path:
        sys.path.append(path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abkayit.settings")
    django.setup()
    karalisteimport()
        
    #except:
    #    print "Project path can not be empty!"
