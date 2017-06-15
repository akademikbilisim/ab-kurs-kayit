# -*- coding:utf-8  -*-

import random
import logging

from django.contrib.auth.models import User

from pysimplesoap.client import SoapClient

from abkayit.settings import TCKIMLIK_SORGULAMA_WS, EMAIL_FROM_ADDRESS
from training.models import Course, TrainessParticipation
from userprofile.models import TrainessNote
'''
    General operations that are used in userprofile app.
'''

log = logging.getLogger(__name__)


class UserProfileOPS:
    def __init__(self):
        pass

    @staticmethod
    def generatenewpass(plen):
        chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijkmnpqrstuvwxyz'
        password = ''.join(random.choice(chars) for i in range(plen))
        return password

    @staticmethod
    def validateTCKimlikNo(tckimlikno, name, surname, year):
        '''

        :param tckimlikno: tc kimlik numarası
        :param name: ad (tam olarak yazılmalı, Türkçe karakter, birden fazla isim varsa aynen yazılmalı)
        :param surname: soyad (tam olarak yazılmalı, Türkçe karakter, birden fazla soyad varsa aynen yazılmalı)
        :param year: doğum yılı
        :return: verilen tc kimlik no verilen bilgideki kişiye mi ait sorgulaması vatandaşlık işlerinden yapılır.
        '''
        try:
            client = SoapClient(wsdl=TCKIMLIK_SORGULAMA_WS, trace=False)
            response = client.TCKimlikNoDogrula(TCKimlikNo=tckimlikno,
                                                Ad=name.replace('i', 'İ').decode('utf-8').upper(),
                                                Soyad=surname.replace('i', 'İ').decode('utf-8').upper(), DogumYili=year)
            return response['TCKimlikNoDogrulaResult']
        except:
            return -1

    @staticmethod
    def is_instructor(uprofile):
        courses = Course.objects.filter(site__is_active=True, trainer=uprofile)
        if courses:
            return True
        else:
            return False

    @staticmethod
    def is_authorized_inst(uprofile, course=None):
        if course:
            if uprofile in course.authorized_trainer.all():
                return True
        else:
            courses = Course.objects.filter(site__is_active=True, authorized_trainer=uprofile)
            if courses:
                return True
        return False

    @staticmethod
    def is_user_trainer_ofcourse_or_staff(user, course):
        '''

        :param user: istegi yapan kullanıcı
        :param course: hangi kurs için yapıldığı
        :return: istegi yapan kullanıcı yetkili eğitmen veya görevli ise True değilse False döner
        '''
        if user.is_staff or user.userprofile in course.authorized_trainer.all():
            return True
        return False

    @staticmethod
    def savenote(request, user, trainessnote):
        '''

        :param request: not kaydetmek için yapılan http istegi
        :return: isteğin içerisinden not ve hangi kullanıcı için istendiği bilgisi alınır ve not formatı uygunsa kaydeder
        geriye hata mesajı ya da başarılı mesajı döner
        '''

        if trainessnote and len(trainessnote) <= 500:
            tnote = TrainessNote(note_to_profile=user.userprofile,
                                 note_from_profile=request.user.userprofile,
                                 note=trainessnote,
                                 site=request.site,
                                 label='egitim')
            alert = "Kursiyer notu başarıyla kaydedildi."
            tnote.save()
        else:
            alert = "Kullanıcı notu en fazla 500 karakter olabilir!!"
        return alert

    @staticmethod
    def saveparticipation(request, courserecord):
        '''

        :param request: yoklamaları kaydetmek için yapılan http isteği
        :param courserecord: hangi kurs kaydı için yoklama girişi yapılacağı
        :return: her gün için gelen post isteğinden sabah, öğlen ve akşam yoklamaları çekilir ve kaydedilir.
        geriye hata mesajı veya başarılı mesajı döner.
        '''
        for date in range(1, int((request.site.event_end_date - request.site.event_start_date).days) + 1):
            morning = request.POST.get("participation" + str(date) + "-morning")
            afternoon = request.POST.get("participation" + str(date) + "-afternoon")
            evening = request.POST.get("participation" + str(date) + "-evening")
            note = 'Seçimleriniz başarıyla kaydedildi.'
            log.info("%s nolu kurs kaydinin yoklama kaydi girişi başarılı" % courserecord.pk,
                     extra=request.log_extra)
            try:
                tp, created = TrainessParticipation.objects.get_or_create(courserecord=courserecord, day=str(date))
                tp.morning = morning
                tp.afternoon = afternoon
                tp.evening = evening
                tp.save()
            except:
                note = 'Hata oluştu!'
                log.info("%s nolu kurs kaydinin yoklama kaydi girişi hatalı" % courserecord.pk,
                         extra=request.log_extra)
        return note
