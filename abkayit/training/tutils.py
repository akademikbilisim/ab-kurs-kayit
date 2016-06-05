#!-*- coding:utf-8 -*-

import logging
from datetime import datetime, timedelta

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from abkayit.models import Site
from abkayit.adaptor import send_email
from abkayit.settings import EMAIL_FROM_ADDRESS, PREFERENCE_LIMIT, ADDITION_PREFERENCE_LIMIT
from abkayit.models import ApprovalDate

from training.models import Course, TrainessCourseRecord, TrainessParticipation
from training.forms import ParticipationForm

log = logging.getLogger(__name__)


def send_pref_saved_email(requestuser, d):
    """
    kursiyer tercih yaptiktan sonra tercih bilgilerinin gonderildiği e-posta
    :param requestuser:
    :param d: loga yazılacak ayrıntılar

    """
    try:
        context = {'user': requestuser}
        domain = Site.objects.get(is_active=True).home_url
        if domain.endswith('/'):
            domain = domain.rstrip('/')
        context['domain'] = domain

        send_email("training/messages/preference_saved_subject.html",
                   "training/messages/preference_saved.html",
                   "training/messages/preference_saved.text",
                   context,
                   EMAIL_FROM_ADDRESS,
                   [requestuser.username])
    except Exception as e:
        log.error(e.message, extra=d)


def send_email_to_inform_trainer(data, d):
    """

    :param data: mail iceriginde kullanilacak veriler
    :param d: logda kullanilacak veriler
    Kurs onaylama sayfasinda yapilan degisiklikler ile ilgili kursun egitmenlerine uyarı e-postası gönderilir.
    """
    try:
        send_email("training/messages/inform_trainers_about_changes_subject.txt",
                   "training/messages/inform_trainers_about_changes.html",
                   "training/messages/inform_trainers_about_changes.txt",
                   data,
                   EMAIL_FROM_ADDRESS,
                   data['course'].trainer.all().values_list('user__username', flat=True))
    except Exception as e:
        log.error(e.message, extra=d)


def get_approve_start_end_dates_for_inst(site, d):
    """

    :param site: aktif etkinliğin sitesi
    :param d: log icin gerekli detaylar
    :return: egitmenin tercih onaylama tarihlerini barındıran bir dictionary geri dondurur.
    """
    dates = {}
    for i in range(1, PREFERENCE_LIMIT + 1):
        try:
            dates[i] = ApprovalDate.objects.get(site=site, preference_order=i, for_instructor=True)
        except:
            log.info("%d tercih sirasina sahip bir ApprovalDate yok" % i, extra=d)
    for i in range(1, ADDITION_PREFERENCE_LIMIT + 1):
        try:
            dates[-i] = ApprovalDate.objects.get(site=site, preference_order=-i, for_instructor=True)
        except:
            log.info("%d tercih sirasina sahip bir ApprovalDate yok" % -i, extra=d)
    return dates


def get_approve_start_end_dates_for_tra(site, d):
    """
        :param site: aktif etkinliğin sitesi
        :param d: log icin gerekli detaylar
        :return: kursiyerler için tercih onaylama tarihlerinin start_date'i en yakin olan ile end_date'i en son olani doner.
    """
    dates = ApprovalDate.objects.filter(site=site, for_trainess=True)
    return dates.order_by("start_date").first(), dates.latest("end_date")


def get_additional_pref_start_end_dates_for_trainess(site, d):
    """

    :param site: aktif etkinliğin sitesi
    :param d: log icin gerekli detaylar
    :return: ek tercih varsa tarihlerini barındıran bir dictionary geri dondurur.
    """
    dates = {}
    for i in range(1, ADDITION_PREFERENCE_LIMIT + 1):
        try:
            dates[-i] = ApprovalDate.objects.get(site=site, preference_order=-i, for_trainess=True)
        except:
            log.info("%d tercih sirasina sahip bir ApprovalDate yok" % -i, extra=d)
    return dates


def get_approved_trainess(course, d):
    """

    :param d: log icin gerekli bilgileri icerir
    :param course: bir kursta onaylanmis kisilerin listesi
    :return: tercih sırasına göre onaylanan kişileri iceren bir dictionary döner.
    """
    trainess = {}
    for i in range(1, PREFERENCE_LIMIT + 1):
        trainess[i] = TrainessCourseRecord.objects.filter(course=course.pk, preference_order=i, approved=True,
                                                          trainess_approved=True).prefetch_related('course')
    for i in range(1, ADDITION_PREFERENCE_LIMIT + 1):
        trainess[-i] = TrainessCourseRecord.objects.filter(course=course.pk, preference_order=-i, approved=True,
                                                           trainess_approved=True).prefetch_related('course')
    return trainess


def get_trainess_by_course(course, d):
    """

    :param d: log icin gerekli bilgileri icerir
    :param course: ilgili kurs
    :return: diger kurslarda onaylanmamış olanların listesini bir dictionary içerisinde döner
    """
    trainess = {}
    for i in range(1, PREFERENCE_LIMIT + 1):
        # trainess[course][i] = TrainessCourseRecord.objects.filter(course=course.pk, preference_order=i).exclude(
        #    trainess__in=TrainessCourseRecord.objects.filter(~Q(course=course.pk), trainess_approved=True).values_list(
        #        'trainess'))
        trainess[i] = TrainessCourseRecord.objects.filter(course=course.pk, preference_order=i).prefetch_related(
            'course')
    for i in range(1, ADDITION_PREFERENCE_LIMIT + 1):
        # trainess[course][-i] = TrainessCourseRecord.objects.filter(course=course.pk, preference_order=-i).exclude(
        #    trainess__in=TrainessCourseRecord.objects.filter(~Q(course=course.pk), trainess_approved=True).values_list(
        #        'trainess'))
        trainess[-i] = TrainessCourseRecord.objects.filter(course=course.pk, preference_order=-i).prefetch_related(
            'course')
    return trainess


def is_trainess_approved_any_course(userprofile, site, d):
    """

    :param userprofile: kullanici profili
    :param site: aktif site
    :param d: log icin gerekli bilgiler
    :return: kullanicinin kabul edildiği bir kurs var mı yok mu onu verir True/False
    """
    try:
        approvedtrainesscourserecords = TrainessCourseRecord.objects.filter(trainess=userprofile,
                                                                            approved=True,
                                                                            trainess_approved=True,
                                                                            course__site=site,
                                                                            preference_order__gte=0)
        if not len(approvedtrainesscourserecords):
            return True
        return False
    except ObjectDoesNotExist as e:
        log.info('%s kullanicisinin onaylanmis kaydi yok.' % userprofile.user.username, extra=d)
        return False


def save_course_prefferences(userprofile, course_prefs, d):
    res = {'status': '-1', 'message': 'error'}
    if len(course_prefs) <= PREFERENCE_LIMIT:
        if len(set([i['value'] for i in course_prefs])) == len([i['value'] for i in course_prefs]):
            for course_pre in course_prefs:
                try:
                    course_record = TrainessCourseRecord(trainess=userprofile,
                                                         course=Course.objects.get(id=course_pre['value']),
                                                         preference_order=course_pre['name'])
                    course_record.save()
                    res['status'] = 0
                    res['message'] = "Tercihleriniz başarılı bir şekilde güncellendi"
                    send_pref_saved_email(userprofile.user, d)
                except Exception as e:
                    log.error(e.message, extra=d)
                    res['message'] = "Tercihleriniz kaydedilirken hata oluştu"
        else:
            res['message'] = "Farklı Tercihlerinizde Aynı Kursu Seçemezsiniz"
    else:
        res['message'] = "En fazla " + PREFERENCE_LIMIT + " tane tercih hakkına sahipsiniz"
    return res


def daterange(start_date, end_date):
    """
    Verilen iki tarih aralığında bir 'iterable' nesne oluşturur. for ... in yapisinin icerisinde kullanilmak uzere
    :param start_date: baslangic tarihi
    :param end_date: bitis tarihi
    """
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def getparticipationforms(site, courserecord):
    rows = []
    for date in daterange(site.event_start_date, site.event_end_date):
        try:
            tp = TrainessParticipation.objects.get(courserecord=courserecord.pk, day=str(date))
            rows.append(ParticipationForm(instance=tp, prefix="participation" + str(date.day)))
        except:
            rows.append(ParticipationForm(initial={'courserecord': courserecord.pk, 'day': str(date)},
                                               prefix="participation" + str(date.day)))
    return rows
