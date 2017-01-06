#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import sys
import os
import django
import re

def get_users_with_edu():
    from userprofile.models import UserProfile
    users = UserProfile.objects.filter(user__username__contains="edu.tr")
    for user in users:
        print user

def application_opens():
    from training.models import Course
    courses = Course.objects.filter(site__is_active=True)
    for course in courses:
        print course.no
        course.application_is_open = True
        course.save()


def onayla():
    from django.contrib.auth.models import User
    from userprofile.models import UserProfile
    from training.models import Course, TrainessCourseRecord
    coursepk = 39  # Kursiyerlerin hangi kurs tercihleri onaylanacak?
    with open(
            "onaylanacaklar") as e:  # Burada onaylanacak kisilerin eposta adreslerinin bulundugu dosya gelecek (her satirda bir adres)
        kursiyerler = e.readlines()
        for k in kursiyerler:
            print k
            ku = User.objects.get(username=k.rstrip())
            kup = UserProfile.objects.get(user=ku)
            kupts = TrainessCourseRecord.objects.filter(trainess=kup).filter(course__pk=coursepk)
            for kupt in kupts:
                print kupt.trainess.user.username
                kupt.approved = True
                kupt.save()
                print kupt.approved


def karalisteimport():
    from userprofile.models import UserProfile, TrainessNote
    from abkayit.models import Site
    from datetime import datetime
    # with open("karaliste.csv.bk") as f:
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
                    #                    trainessnote = TrainessNote(site=site, note_to_profile=userobj[0],
                    #                                                note_from_profile=UserProfile.objects.get(
                    #                                                    user__username="ozge@kripton.rocks"), label="sistem",
                    #                                                note=userfields[5])
                    #                    trainessnote.save()
                    print "*******"
                    print userfields[0]
                    print userobj
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
                        trainessnote = TrainessNote(site=site, note_to_profile=userobj2[0],
                                                    note_from_profile=UserProfile.objects.get(
                                                        user__username="ozge@kripton.rocks"), label="sistem",
                                                    note=userfields[5])
                        trainessnote.save()
                        print "*******"
                        print userfields[0]
                        print userobj2
                        # pass
                    else:
                        print "******* Profil var site yok"
                        print userfields[0]
                        print userobj2


def push_note_to_trainess(note, filename):
    from userprofile.models import UserProfile, TrainessNote
    from abkayit.models import Site
    if note and filename:
        site = Site.objects.get(is_active=True)  # FIXME is_active birden fazla olabilir!
        fromup = UserProfile.objects.get(user__username="ozge@kripton.rocks")
        with open(filename) as f:
            userlist = f.readlines()
            for user in userlist:
                print user
                usermail = user.rstrip()
                up = UserProfile.objects.get(user__username=usermail)
                # trainessnote = TrainessNote.objects.get(note_to_profile=up)
                # trainessnote.note = note
                # trainessnote.save()
                trainessnote = TrainessNote(site=site, note_to_profile=up, note_from_profile=fromup, label="sistem",
                                            note=note)
                trainessnote.save()
    else:
        print "note and filename can not be empty!!"


def import_participation(filename):
    from training.models import TrainessCourseRecord, TrainessParticipation
    with open(filename) as f:
        tcrlist = f.readlines()  # trainess course record id listesi
        for tcrno in tcrlist:
            tcrnoint = int(re.search(r'\d+', tcrno.rstrip()).group())
            tcr = TrainessCourseRecord.objects.get(pk=tcrnoint)
            print tcr
            for i in range(1, 17):
                print i
                trp = TrainessParticipation(courserecord=tcr, day=i, morning='2', afternoon='2', evening='2')
                trp.save()


if __name__ == "__main__":
    # try:
    path = sys.argv[1]
    if path not in sys.path:
        sys.path.append(path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abkayit.settings")
    django.setup()
#    get_users_with_edu()
    application_opens()
    # karalisteimport()
    # push_note_to_trainess("note", "filename")
#    import_participation("lyk2016_kabuledilenler_tercihno.csv")
    # except:
    #    print "Project path can not be empty!"
