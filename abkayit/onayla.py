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
    coursesin = ['36', '50', '61', '105', '121', '126', '40']
    courses = Course.objects.filter(site__is_active=True, no__in=coursesin)
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

def correct_wrongs():
    from training.models import TrainessCourseRecord
    wrongs = TrainessCourseRecord.objects.filter(consentemailsent=True,approved=False,course__site__is_active=True)
    for w in wrongs:
        print "\n"
        print "First approve", w.trainess, w.course
        wrongapprove = TrainessCourseRecord.objects.get(trainess=w.trainess, consentemailsent=True, approved=True,course__site__is_active=True)
        print wrongapprove
        wrongapprove.consentemailsent = False
        wrongapprove.approved = False
        wrongapprove.trainess_approved = False
        wrongapprove.save()
        print "Second approve", wrongapprove.trainess, wrongapprove.course
        w.consentemailsent = True
        w.approved = True
        w.trainess_approved = True
        w.save()
        print "change successful"

def cancel_course(course_no):
    from training.models import TrainessCourseRecord
    from django.db.models import Q
   
    linux3tercih_edenler = TrainessCourseRecord.objects.filter(course__no=course_no, course__site__is_active=True)
    for tercih in linux3tercih_edenler:
        print tercih.trainess
        diger_tercihleri = TrainessCourseRecord.objects.filter(trainess=tercih.trainess).filter(~Q(course__no=course_no))
        if tercih.preference_order == 1:
            for dtercih in diger_tercihleri:
                if dtercih.preference_order == 2:
                    dtercih.preference_order=1
                    dtercih.save()
                    print dtercih.pk
                    print "preference order changed to 1"
                elif dtercih.preference_order == 3:
                    dtercih.preference_order=2
                    dtercih.save()
                    print dtercih.pk
                    print "preference order changed to 2"
        if tercih.preference_order == 2:
            for dtercih in diger_tercihleri:
                if dtercih.preference_order == 3:
                    dtercih.preference_order=2
                    dtercih.save()
                    print dtercih.pk
                    print "preference order changed to 2"
        tercih.delete()
def write_par():
    from abkayit.models import Site
    from training.models import Course, TrainessCourseRecord, TrainessParticipation
    
    gelmeyenler_dict = {}
    print "parsing text file..."
    with open("ab2017_gelmeyenler.txt", "r") as f:
        kisiler=  f.readlines()
        for kisi in kisiler:
            print kisi
            course_no =  kisi.split("-")[0]
            isim_soyisim =  kisi.split("-")[1].rstrip("\n")
            course = Course.objects.get(pk=course_no)
            try:
                gelmeyenler_dict[course.pk].append(isim_soyisim)
            except:
                gelmeyenler_dict[course.pk] = [isim_soyisim]
    
    print "participation..."
    site = Site.objects.get(name__contains="Akademik Bil", year="2017")
    courses = Course.objects.filter(site=site)
    print courses
    print "hebelek"
    for c in courses:
        print "hebelek 2"
        tcrs = TrainessCourseRecord.objects.filter(course=c, approved=True)
        print tcrs
        for tcr in tcrs:
            print tcr.pk
            kursiyer_ismi = tcr.trainess.user.first_name + " " + tcr.trainess.user.last_name
            gelmeyenlerlist = gelmeyenler_dict.get(c.pk, None)
            if gelmeyenlerlist and kursiyer_ismi not in gelmeyenler_dict[c.pk]:
                for i in range(1, 5):
                    trp = TrainessParticipation(courserecord=tcr,day=i, morning="2", afternoon="2", evening="-1")
                    trp.save()
            else:
                for i in range(1, 5):
                    trp = TrainessParticipation(courserecord=tcr,day=i, morning="0", afternoon="0", evening="-1")
                    trp.save()
    else:
         print "bos" 

if __name__ == "__main__":
    # try:
    path = sys.argv[1]
    if path not in sys.path:
        sys.path.append(path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abkayit.settings")
    django.setup()
#    get_users_with_edu()
#    application_opens()
    #correct_wrongs()
    #cancel_course('3')
    write_par()
    # karalisteimport()
    # push_note_to_trainess("note", "filename")
#    import_participation("lyk2016_kabuledilenler_tercihno.csv")
    # except:
    #    print "Project path can not be empty!"
