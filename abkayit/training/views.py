# -*- coding: utf-8 -*-

import json
import logging
import itertools
from datetime import datetime

from django.shortcuts import render_to_response, RequestContext, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone

from abkayit.backend import getsiteandmenus
from abkayit.models import Site, Menu, ApprovalDate, Answer
from abkayit.decorators import active_required
from abkayit.settings import PREFERENCE_LIMIT, ADDITION_PREFERENCE_LIMIT, EMAIL_FROM_ADDRESS, REQUIRE_TRAINESS_APPROVE

from userprofile.models import UserProfile, TrainessNote, TrainessClassicTestAnswers
from userprofile.forms import InstProfileForm, CreateInstForm
from userprofile.userprofileops import UserProfileOPS

from training.models import Course, TrainessCourseRecord
from training.forms import CreateCourseForm, ParticipationForm, AddTrainessForm
from training.tutils import get_approve_start_end_dates_for_inst, save_course_prefferences, applytrainerselections
from training.tutils import get_approve_start_end_dates_for_tra, get_additional_pref_start_end_dates_for_trainess
from training.tutils import get_approved_trainess, get_trainess_by_course, is_trainess_approved_any_course, \
    gettestsofcourses

log = logging.getLogger(__name__)

DATETIME_FORMAT = "%d/%m/%Y %H:%M"


@login_required
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def show_course(request, course_id):
    try:
        data = getsiteandmenus(request)
        course = Course.objects.get(id=course_id)
        data['course'] = course
        return render_to_response('training/course_detail.html', data, context_instance=RequestContext(request))
    except ObjectDoesNotExist:
        return HttpResponse("Kurs Bulunamadi")


@login_required
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def list_courses(request):
    data = getsiteandmenus(request)
    courses = Course.objects.filter(site=data['site'])
    data['courses'] = courses
    return render_to_response('training/courses.html', data, context_instance=RequestContext(request))


@login_required
def apply_to_course(request):
    """
    controlpanel view'ında userprofile ogrenci ise buraya yonleniyor
    tercih zamanı ve ek tercih zamanı burada gorunuyor.
    :param request:
    :return: kullanıcı tercih zamanı eğer sıkca sorulan sorulara doğru yanıt vermisse PREFERENCE_LIMIT kadar tercih yapar
      eger profili yoksa createprofile yönlendirilir
      eger sıkca sorulan sorulara cevap vermemisse sıkca sorulan sorulara yonlendirilir.
    """
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    data['closed'] = True
    data['additional1_pref_closed'] = True
    data['PREFERENCE_LIMIT'] = PREFERENCE_LIMIT
    data['ADDITION_PREFERENCE_LIMIT'] = ADDITION_PREFERENCE_LIMIT
    now = datetime.now()
    data['may_cancel_all'] = True if data['site'].event_start_date > datetime.date(now) else False
    """
    courses: mevcut etkinte onaylanmis ve basvuruya acik kurslar
    """
    data['courses'] = Course.objects.filter(approved=True, site=data['site'], application_is_open=True)
    """
    course_records: katilimcinin, mevcut etkinlikteki tercihleri
    """
    data['course_records'] = TrainessCourseRecord.objects.filter(trainess__user=request.user,
                                                                 course__site__is_active=True).order_by('preference_order')
    userprofile = request.user.userprofile
    if not userprofile:
        log.info("userprofile not found", extra=d)
        return redirect("createprofile")
    if data['courses']:
        if data['site'].application_start_date <= datetime.date(now) <= data['site'].application_end_date:
            log.info("in between application start and end date", extra=d)
            if userprofile.userpassedtest:
                data['closed'] = False
                note = _("You can choose courses in order of preference.")
                if request.GET:
                    course_prefs = request.GET
                    pref_tests = gettestsofcourses(course_prefs)
                    if pref_tests:
                        data['note'] = "Lutfen asağidaki soruları yanıtlayın"
                        data['pref_tests'] = pref_tests
                        if "submitanswers" in request.POST:
                            answersforcourse = {}
                            for course, questions in pref_tests.items():
                                answersforcourse[course] = []
                                for question in questions[0]:
                                    uansw = request.POST.get(str(course.pk) + str(question.no))
                                    ranswer = Answer.objects.get(pk=int(uansw))
                                    if ranswer:
                                        answersforcourse[course].append(ranswer)
                                    else:
                                        data["note"] = "Lütfen tüm soruları doldurun!"
                                        return render_to_response("training/testforapplication.html", data,
                                                                  context_instance=RequestContext(request))
                                for question in questions[1]:
                                    tbansw = request.POST.get("answer" + str(question.pk))
                                    if tbansw:
                                        tcta, created = TrainessClassicTestAnswers.objects.get_or_create(
                                            user=request.user.userprofile, question=question)
                                        tcta.answer = tbansw
                                        tcta.save()
                            res = save_course_prefferences(userprofile, course_prefs, data['site'], d,
                                                           answersforcourse=answersforcourse)
                            data['note'] = res['message']
                            return render_to_response("training/applytocourse.html", data,
                                                      context_instance=RequestContext(request))
                        return render_to_response("training/testforapplication.html", data,
                                                  context_instance=RequestContext(request))
                    else:
                        res = save_course_prefferences(userprofile, course_prefs, data['site'], d)
                        data['note'] = res['message']
                    data['note'] = res['message']
                    return render_to_response("training/applytocourse.html", data,
                                              context_instance=RequestContext(request))
                data['note'] = note
            else:
                return redirect("testbeforeapply")
        elif datetime.date(now) < data['site'].application_start_date:
            log.info("before application start date", extra=d)
            data['note'] = "Tercih dönemi %s tarihinde açılacaktır" % data['site'].application_start_date
        elif datetime.date(now) > data['site'].application_end_date:
            log.info("after application end date", extra=d)
            data[
                'note'] = "Tercih dönemi %s tarihinde kapanmıştır. Başvuru durumunuzu İşlemler> Başvuru Durum/Onayla " \
                          "adımından görüntüleyebilirsiniz " % data['site'].application_end_date
            """
             Bu kod parcasi ek tercihler icindir. Eger kullanıcının kabul ettigi ve edildigi bir kurs yoksa ve
             ek tercih aktifse bu kod blogu calisir.
            """
            if ADDITION_PREFERENCE_LIMIT:
                adates = get_additional_pref_start_end_dates_for_trainess(data['site'], d)
                if adates:
                    for adate in adates:
                        if adates[adate].start_date <= now <= adates[adate].end_date:
                            if is_trainess_approved_any_course(userprofile, data['site'], d):
                                data['additional1_pref_closed'] = False
                                log.info("ek tercih aktif", extra=d)
                                data['note'] = _("You can make additional preference.")
    else:
        data['note'] = _("There isn't any course in this event.")
    return render_to_response('training/applytocourse.html', data)


@login_required
def testforapplication(request):
    data = getsiteandmenus(request)

    return render_to_response("testforapplication.html", data, context_instance=RequestContext(request))


@login_required
def approve_course_preference(request):
    """
    Bu view katilimci bir kursa kabul edilip edilmedigini görüntülemesi ve katilimcidan katılıp katılmayacağına dair
    son bir teyit alınır.
    :param request: HttpRequest
    :return:
    """
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    message = ""
    status = "1"
    data = getsiteandmenus(request)
    now = timezone.now()
    trainess_course_record = None
    try:
        first_start_date, last_end_date = get_approve_start_end_dates_for_tra(data['site'], d)
        data["approve_is_open"] = False
        note = "Başvuru Durumunuz"
        recordapprovedbyinst = TrainessCourseRecord.objects.filter(trainess=request.user.userprofile, approved=True,
                                                                   course__site=data['site'])
        recordapprovedbytra = recordapprovedbyinst.filter(trainess_approved=True)
        if first_start_date and last_end_date and REQUIRE_TRAINESS_APPROVE:
            if first_start_date.start_date < now < last_end_date.end_date:
                if not recordapprovedbyinst:
                    note = "Henüz herhangi bir kursa kabul edilemediniz."
                elif not recordapprovedbytra and recordapprovedbyinst:
                    note = "Aşağıdaki kursa kabul edildiniz"
                    for record in recordapprovedbyinst:
                        pref_order = record.preference_order
                        approvedate = ApprovalDate.objects.get(site=data['site'], preference_order=pref_order)
                        if approvedate.start_date <= now <= approvedate.end_date:
                            data["approve_is_open"] = True
                            trainess_course_record = record
                else:
                    trainess_course_record = recordapprovedbytra[0]
                    note = "Aşağıdaki Kursa Kabul Edildiniz"
            else:
                if recordapprovedbytra:
                    note = "Aşağıdaki Kursa Kabul Edildiniz"
                    trainess_course_record = recordapprovedbytra[0]
                elif recordapprovedbyinst:
                    note = "Aşağıdaki kursa kabul edildiniz ancak teyit etmediniz. Kursa katılamazsınız."
                    trainess_course_record = recordapprovedbyinst[0]
                else:
                    note = "Henüz kabul edildiğiniz bir kurs yok"
        else:
            if recordapprovedbytra:
                note = "Aşağıdaki kursa kabul edildiniz"
                trainess_course_record = recordapprovedbytra[0]
            else:
                note = "Kabul edildiğiniz bir kurs bulunmamakta"
        data['note'] = note
    except Exception as e:
        log.error(e.message, extra=d)
        data['note'] = "Hata oluştu"
    if request.POST:
        try:
            log.debug(request.POST.get("courseRecordId"), extra=d)
            if request.POST.get("courseRecordId") and trainess_course_record:
                trainess_course_record.trainess_approved = True
                trainess_course_record.save()
                message = "İşleminiz başarılı bir şekilde gerçekleştirildi"
                status = "0"
                log.debug("kursu onayladi " + trainess_course_record.course.name, extra=d)
        except Exception as e:
            log.error(e.message, extra=d)
            message = "İşleminiz Sırasında Hata Oluştu"
            status = "-1"
        return HttpResponse(json.dumps({'status': status, 'message': message}), content_type="application/json")
    data['trainess_course_record'] = trainess_course_record
    return render_to_response("training/confirm_course_preference.html", data)


@login_required
def control_panel(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    note = _("You can accept trainees")
    now = timezone.now()
    data["user"] = request.user
    try:
        if UserProfileOPS.is_instructor(request.user.userprofile):
            courses = Course.objects.filter(site=data['site'], approved=True, trainer__user=request.user)
            log.info(courses, extra=d)
            if courses:
                log.info("egitmenin " + str(len(courses)) + " tane kursu var", extra=d)
                data['now'] = now
                data['dates'] = get_approve_start_end_dates_for_inst(data['site'], d)
                data['trainess'] = {}
                if data['dates']:
                    for course in courses:
                        if now <= data['dates'].get(1).end_date:
                            data['trainess'][course] = get_trainess_by_course(course, d)
                        else:
                            note = _("Consent period is closed")
                            data['trainess'][course] = get_approved_trainess(course, d)
                if "send" in request.POST:
                    log.info("kursiyer onay islemi basladi", extra=d)
                    log.info(request.POST, extra=d)
                    note = applytrainerselections(request.POST, courses, data, d)
            data['note'] = note
            return render_to_response("training/controlpanel.html", data, context_instance=RequestContext(request))
        elif not request.user.is_staff:
            return redirect("applytocourse")
        return redirect("statistic")
    except UserProfile.DoesNotExist:
        return redirect("createprofile")


@staff_member_required
def allcourseprefview(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    data['datalist'] = TrainessCourseRecord.objects.filter(course__site=data['site'])
    return render_to_response("training/allcourseprefs.html", data, context_instance=RequestContext(request))


@staff_member_required
def statistic(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    try:
        data = getsiteandmenus(request)

        record_data = TrainessCourseRecord.objects.filter(course__site__is_active=True).values(
            'course', 'preference_order').annotate(
            Count('preference_order')).order_by(
            'course', '-preference_order')
        statistic_by_course = {}
        for key, group in itertools.groupby(record_data, lambda item: item["course"]):
            course_object = Course.objects.get(pk=key, site__is_active=True)
            statistic_by_course[course_object] = {str(item['preference_order']): item['preference_order__count'] for
                                                  item in group}
            statistic_by_course[course_object]['total_apply'] = len(TrainessCourseRecord.objects.filter(
                course=course_object))
            statistic_by_course[course_object]['total_apply_by_trainer'] = len(TrainessCourseRecord.objects.filter(
                course=course_object, approved=True))
            statistic_by_course[course_object]['total_apply_by_trainess'] = len(TrainessCourseRecord.objects.filter(
                course=course_object, approved=True, trainess_approved=True))

        data['statistic_by_course'] = statistic_by_course
        # statistic_by_gender = UserProfile.objects.filter(is_instructor=False).filter(
        #    trainesscourserecord__course__site__is_active__in=[True]).values('gender').annotate(
        #    Count('gender')).order_by('gender')
        # data['statistic_by_gender'] = statistic_by_gender
        # statistic_by_gender_for_approved = UserProfile.objects.filter(is_instructor=False).filter(
        #    trainesscourserecord__approved=[True], trainesscourserecord__course__site__is_active__in=[True]).filter(
        #    trainesscourserecord__trainess_approved__in=[True]).values('gender').annotate(Count('gender')).order_by(
        #    'gender')
        # data['statistic_by_gender_for_approved'] = statistic_by_gender_for_approved
        # log.debug(statistic_by_gender, extra=d)
        # statistic_by_university = UserProfile.objects.filter(is_instructor=False).filter(
        #    trainesscourserecord__course__site__is_active__in=[True]).values('university').annotate(
        #    Count('university')).order_by('-university__count')
        # data['statistic_by_university'] = statistic_by_university
        #
        # statistic_by_university_for_approved = UserProfile.objects.filter(is_instructor=False).values(
        #    'university').filter(trainesscourserecord__course__site__is_active__in=[True],
        #                         trainesscourserecord__approved__in=[True]).filter(
        #    trainesscourserecord__trainess_approved__in=[True]).annotate(Count('university')).order_by(
        #    '-university__count')
        # data['statistic_by_university_for_approved'] = statistic_by_university_for_approved

        # kurs bazinda toplam teyitli olanlar
        data['statistic_by_course_for_apply'] = TrainessCourseRecord.objects.filter(course__site__is_active=True,
                                                                                    approved=True).values(
            'course__name').annotate(count=Count('course')).order_by('-count')
        total_profile = len(
            TrainessCourseRecord.objects.filter(course__site__is_active=True).order_by("trainess").values(
                "trainess").distinct())
        total_preference = len(TrainessCourseRecord.objects.filter(course__site__is_active=True))
        total_preference_for_approved = len(
            TrainessCourseRecord.objects.filter(course__site__is_active=True, approved=True))
        data['statistic_by_totalsize'] = {'Toplam Profil(Kişi)': total_profile, 'Toplam Tercih': total_preference,
                                          'Toplam Teyit Eden': total_preference_for_approved}
    except Exception as e:
        log.error(e.message, extra=d)
    return render_to_response("training/statistic.html", data)


@login_required
def cancel_all_preference(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    userprofile = UserProfile.objects.get(user=request.user)
    now_for_approve = timezone.now()
    if request.POST:
        try:
            cancelnote = request.POST.get('cancelnote', '')
            trainess_course_records = TrainessCourseRecord.objects.filter(course__site__is_active=True,
                                                                          trainess=userprofile)
            context = {}
            approvedpref = None
            for tcr in trainess_course_records:
                try:
                    # x. tercih onaylama donemi baslangic zamani ile x. tercih teyit etme donemi arasinda ise mail atsin.
                    if tcr.approved:
                        approvedpref = tcr
                    if data['site'].application_end_date < datetime.date(datetime.now()) < data['site'].event_start_date:
                        if tcr.trainess_approved:
                            context['trainess_course_record'] = tcr
                            context['recipientlist'] = tcr.course.authorized_trainer.all().values_list(
                                'user__username', flat=True)
                            send_email_by_operation_name(context, "notice_for_canceled_prefs")
                except Exception as e:
                    log.error(e.message, extra=d)
                trainess_course_records.delete()
            if data['site'].application_end_date < datetime.date(now_for_approve):
                remaining_days = int((data['site'].event_start_date - datetime.date(now_for_approve)).days)
                notestr = "Kursların başlamasına %d gun kala tüm başvurularını iptal etti." % remaining_days
                if approvedpref:
                    # Kullanicinin tercihi kursa kaç gün kala kabul görmüş
                    daysbetweenapproveandevent = int(
                        (data['site'].event_start_date - approvedpref.instapprovedate).days)
                    notestr += "\nTercihi kursun başlamasına %d gün kala kabul edilmiş." % daysbetweenapproveandevent
            else:
                notestr = "Kullanici tercihlerini iptal etti"
            if cancelnote:
                notestr += "\nİptal Sebebi:%s" % cancelnote
            if notestr:
                note = TrainessNote(note=notestr, note_from_profile=userprofile, note_to_profile=userprofile,
                                    site=data['site'], note_date=now_for_approve, label="sistem")
                note.save()
            message = "Tüm Başvurularınız Silindi"
            log.debug(message, extra=d)
        except ObjectDoesNotExist:
            message = "Başvurularınız Silinirken Hata Oluştu"
        except Exception as e:
            message = "Başvurularınız Silinirken Hata Oluştu"
            log.error(e.message, extra=d)
        return HttpResponse(json.dumps({'status': '-1', 'message': message}), content_type="application/json")
    message = "Başvurularınız Silinirken Hata Oluştu"
    return HttpResponse(json.dumps({'status': '-1', 'message': message}), content_type="application/json")


# 52 numarali issue ile kapatildi
# @login_required
# def cancel_course_application(request):
#    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
#    message = ""
#    status = "-1"
#    if request.POST:
#        try:
#            course = Course.objects.get(id=request.POST.get("course"), approved=True, trainer__user=request.user)
#            if request.POST.get("isOpen") == "true":
#                course.application_is_open = True
#                message = "Bu Kurs İçin Başvurular Açıldı"
#                status = "0"
#            else: 
#                course.application_is_open = False
#                message = "Bu Kurs İçin Başvurular Kapandı"
#                status = "0"
#            course.save()
#        except ObjectDoesNotExist:
#            message = "İşleminiz Sırasında Hata Oluştu"
#            status = "-1"
#        except Exception as e:
#            message = "İşleminiz Sırasında Hata Oluştu"
#            status = "-1"
#            log.error(e.message, extra=d) 
#        return HttpResponse(json.dumps({'status':'-1', 'message':message}), content_type="application/json")
#    message = "İşleminiz Sırasında Hata Oluştu"
#    return HttpResponse(json.dumps({'status':'-1', 'message':message}), content_type="application/json")


@login_required
def get_preferred_courses(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    if request.POST:
        preferred_courses = []
        try:
            course_records = TrainessCourseRecord.objects.filter(course__site__is_active=True, trainess__user=request.user).order_by(
                'preference_order')
            preferred_courses = [course_record.course.name for course_record in course_records]
            status = "0"
        except Exception as e:
            status = "-1"
            log.error(e.message, extra=d)
        return HttpResponse(json.dumps({'status': status, 'preferred_courses': preferred_courses}),
                            content_type="application/json")
    return HttpResponse(json.dumps({'status': '-1'}), content_type="application/json")


@login_required
def apply_course_in_addition(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    if request.method == "POST":
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect("createprofile")
        TrainessCourseRecord.objects.filter(course__site__is_active=True, trainess=userprofile).delete()
        course_prefs = json.loads(request.POST.get('course'))
        if len(course_prefs) <= ADDITION_PREFERENCE_LIMIT:
            if len(set([i['value'] for i in course_prefs])) == len([i['value'] for i in course_prefs]):
                for course_pre in course_prefs:
                    try:
                        course_object = Course.objects.get(id=course_pre['value'])
                        if course_object.application_is_open:
                            course_record = TrainessCourseRecord(trainess=userprofile,
                                                                 course=course_object,
                                                                 preference_order=(-1) * int(course_pre['name']))
                            course_record.save()
                            log.debug("ek tercih kaydedildi " + str(course_pre['value']), extra=d)
                        else:
                            message = "Kurs basvurulara kapali"
                            log.error(message + " " + str(course_pre['value']), extra=d)
                    except Exception as e:
                        log.error(e.message, extra=d)
                        message = "Tercihleriniz kaydedilirken hata oluştu"
                        return HttpResponse(json.dumps({'status': '-1', 'message': message}),
                                            content_type="application/json")
                message = "Tercihleriniz başarılı bir şekilde güncellendi"
                return HttpResponse(json.dumps({'status': '0', 'message': message}), content_type="application/json")
    message = "Tercih işlemi yapmanıza izin verilmiyor"
    return HttpResponse(json.dumps({'status': '-1', 'message': message}), content_type="application/json")


@login_required
def addtrainess(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    now = datetime.date(datetime.now())
    if UserProfileOPS.is_authorized_inst(request.user.userprofile) and data['site'].event_start_date > now > data[
        'site'].application_end_date:
        data['form'] = AddTrainessForm(ruser=request.user)
        data['note'] = "Kursunuza eklemek istediğiniz katilimciyi seçin (E-posta adresine göre)"
        if "add" in request.POST:
            data['form'] = AddTrainessForm(request.POST, ruser=request.user)
            if data['form'].is_valid():
                tcourserecord = data['form'].save(commit=False)
                tcourserecord.preference_order = 1
                tcourserecord.trainess_approved = True
                tcourserecord.approved = True
                tcourserecord.save()
                notestr = "Bu kullanicinin %s kursu tercihi eğitmen tarafından eklendi." % tcourserecord.course.name
                note = TrainessNote(note=notestr, note_from_profile=request.user.userprofile,
                                    note_to_profile=tcourserecord.trainess,
                                    site=tcourserecord.course.site, note_date=timezone.now(), label="tercih")
                note.save()
                data['note'] = "Form kaydedildi. Eklediğiniz katılımcıları 1. tercih listesinde görüntüleyebilirsiniz."
                log.info("%s kullanicisi %s kullanicisini %s kursuna ekledi." % (
                    request.user.username, tcourserecord.user.username, tcourserecord.course.name), extra=d)
            else:
                data['note'] = "Form aşağıdaki sebeplerden dolayı kaydedilemedi."
        elif "cancel" in request.POST:
            return redirect("controlpanel")
        return render_to_response('training/addtrainess.html', data, context_instance=RequestContext(request))
    else:
        return redirect("controlpanel")


@staff_member_required
def participationstatuses(request):
    """
    Admin veya is_staff yetkisi verilmiş başka bir kullanıcı ile buraya view ile yoklama kaydı girilecek.
    :param request: HttpRequest
    """
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    data['allcourses'] = Course.objects.filter(site=data['site'])
    data['note'] = "İşlem yapmak istediğiniz kursu seçiniz."
    return render_to_response('training/participationstatuses.html', data, context_instance=RequestContext(request))


@staff_member_required
def editparticipationstatusebycourse(request, courseid):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    data['courserecords'] = TrainessCourseRecord.objects.filter(course__pk=int(courseid), approved=True)
    data['note'] = "Yoklama bilgilerini girmek için kullanıcı profiline gidiniz."
    return render_to_response('training/courseparstatus.html', data, context_instance=RequestContext(request))


#  submitandregister, new_course, edit_course viewlari kullanılmıyor.


@login_required
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def submitandregister(request):
    """
    Bu view'ı kullanmıyoruz. Egitmen ve egitim başvurularını sistemden aldığımızda kullanılabilir.
    :param request:
    :return:
    """
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    userops = UserProfileOPS()
    data = getsiteandmenus(request)
    note = "Kurs onerisi olustur:"
    curinstprofform = InstProfileForm(prefix="cur")
    forms = {}
    for x in xrange(4):
        forms[x] = [CreateInstForm(prefix=str(x) + "inst"), InstProfileForm(prefix=str(x) + "instprof")]
    form = CreateCourseForm()
    if "submit" in request.POST:
        allf = []
        forms = {}
        for x in xrange(4):
            if str(x) + "inst-email" in request.POST:
                forms[x] = [CreateInstForm(request.POST, prefix=str(x) + "inst"),
                            InstProfileForm(request.POST, prefix=str(x) + "instprof")]
                allf.append(forms[x][0].is_valid())
                allf.append(forms[x][1].is_valid())
            else:
                pass
        curinstprofform = InstProfileForm(request.POST, prefix="cur")
        form = CreateCourseForm(request.POST)
        if all([curinstprofform.is_valid(), form.is_valid()]) and all(allf):
            curinst = curinstprofform.save(commit=False)
            curinst.user = request.user
            curinst.save()
            course = form.save(commit=False)
            if 'fulltext' in request.FILES:
                course.fulltext = request.FILES['fulltext']
            course.save()
            for key, f in forms.items():
                instx = f[0].save(commit=False)
                passwd = userops.generatenewpass(8)
                instx.set_password(passwd)
                instx.save()
                instxprof = f[1].save(commit=False)
                instxprof.user = instx
                instxprof.save()
                course.trainer.add(instxprof)
            course.trainer.add(curinst)
            course.save()
            note = "Egitim oneriniz basari ile alindi."
        else:
            note = "Olusturulamadi"
    data['note'] = note
    data['form'] = form
    data['curinstprofform'] = curinstprofform
    data['forms'] = forms
    return render_to_response("training/submitandregister.html",
                              data,
                              context_instance=RequestContext(request))
