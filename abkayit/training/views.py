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
from abkayit.adaptor import send_email
from abkayit.models import Site, Menu, ApprovalDate
from abkayit.decorators import active_required
from abkayit.settings import PREFERENCE_LIMIT, ADDITION_PREFERENCE_LIMIT, EMAIL_FROM_ADDRESS, REQUIRE_TRAINESS_APPROVE

from userprofile.models import UserProfile, TrainessNote
from userprofile.forms import InstProfileForm, CreateInstForm
from userprofile.userprofileops import UserProfileOPS

from training.models import Course, TrainessCourseRecord
from training.forms import CreateCourseForm, ParticipationForm
from training.tutils import *

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
                                                                 course__site=data['site']).order_by('preference_order')
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
                if request.method == "POST":
                    TrainessCourseRecord.objects.filter(trainess=userprofile).delete()
                    course_prefs = json.loads(request.POST.get('course'))
                    res = save_course_prefferences(userprofile, course_prefs, d)
                    return HttpResponse(json.dumps(res), content_type="application/json")
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
                                data['note'] = _("Ek tercih dönemi içindesiniz, ek tercih yapabilirsiniz")
    else:
        data['note'] = _("Etkinlikte henüz kurs yok.")
    return render_to_response('training/applytocourse.html', data)


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
        recordapprovedbyinst = TrainessCourseRecord.objects.filter(trainess=request.user.userprofile, approved=True)
        recordapprovedbytra = recordapprovedbyinst.filter(trainess_approved=True)
        if first_start_date and last_end_date:
            if first_start_date.start_date < now < last_end_date.end_date:
                if not recordapprovedbyinst:
                    note = "Henüz herhangi bir kursa kabul edilemediniz."
                elif not recordapprovedbytra and recordapprovedbyinst:
                    note = "Kabul edildiğiniz aşağıdaki kursu onaylayabilirsiniz"
                    for record in recordapprovedbyinst:
                        pref_order = record.preference_order
                        approvedate = ApprovalDate.objects.get(preference_order=pref_order)
                        if approvedate.start_date < now < approvedate.end_date:
                            data["approve_is_open"] = True
                            trainess_course_record = record
                elif recordapprovedbytra:
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
                    note = "Kurs teyit dönemi dışındasınız veya kabul edildiğiniz kurs yok"
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
    try:
        if not request.user.userprofile.is_student:
            courses = Course.objects.filter(site=data['site'], approved=True, trainer__user=request.user)
            log.info(courses, extra=d)
            if courses:
                log.info("egitmenin " + str(len(courses)) + " tane kursu var", extra=d)
                data['now'] = now
                data['dates'] = get_approve_start_end_dates_for_inst(data['site'], d)
                data['trainess'] = {}
                if data['dates']:
                    for course in courses:
                        if now < data['dates'].get(1).end_date:
                            data['trainess'][course] = get_trainess_by_course(course, d)
                        else:
                            note = _("Kursiyer kabul dönemi kapanmıştır")
                            data['trainess'][course] = get_approved_trainess(course, d)
                if request.POST:
                    log.info("kursiyer onay islemi basladi", extra=d)
                    log.info(request.POST, extra=d)
                    for course in courses:
                        try:
                            approvedr = request.POST.getlist('students' + str(course.pk))
                            allprefs = []
                            for pref in data['dates']:
                                if data['dates'][pref].start_date < now < data['dates'][pref].end_date:
                                    allprefs.extend(TrainessCourseRecord.objects.filter(course=course.pk).filter(
                                        preference_order=pref))
                                    log.debug(allprefs, extra=d)
                            for p in allprefs:
                                if str(p.pk) not in approvedr:
                                    p.approved = False
                                elif str(p.pk) in approvedr:
                                    p.approved = True
                                    p.instapprovedate = now
                                    if not REQUIRE_TRAINESS_APPROVE:
                                        p.trainess_approved = True
                                p.save()
                                log.debug(p, extra=d)
                            course.trainess.clear()
                            allprefs = TrainessCourseRecord.objects.filter(course=course.pk)
                            for p in allprefs:
                                if p.approved:
                                    course.trainess.add(p.trainess)
                            course.save()
                            data["user"] = request.user
                            data["course"] = course
                            note = "Seçimleriniz başarılı bir şekilde kaydedildi."
                        except Exception as e:
                            note = "Beklenmedik bir hata oluştu!"
                            log.error(e.message, extra=d)
            data['note'] = note
            return render_to_response("training/controlpanel.html", data, context_instance=RequestContext(request))
        else:
            return redirect("applytocourse")
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

        record_data = TrainessCourseRecord.objects.filter().values(
            'course', 'preference_order').annotate(
            Count('preference_order')).order_by(
            'course', '-preference_order')
        statistic_by_course = {}
        for key, group in itertools.groupby(record_data, lambda item: item["course"]):
            course_object = Course.objects.get(pk=key)
            statistic_by_course[course_object] = {str(item['preference_order']): item['preference_order__count'] for
                                                  item in group}
            statistic_by_course[course_object]['total_apply'] = len(TrainessCourseRecord.objects.filter(
                course=course_object))
            statistic_by_course[course_object]['total_apply_by_trainer'] = len(TrainessCourseRecord.objects.filter(
                course=course_object).filter(
                approved=True))
            statistic_by_course[course_object]['total_apply_by_trainess'] = len(TrainessCourseRecord.objects.filter(
                course=course_object).filter(
                approved=True).filter(
                trainess_approved=True))
            statistic_by_course[course_object]['total_attended'] = len(TrainessCourseRecord.objects.filter(
                course=course_object).filter(
                approved=True).filter(
                trainess_approved=True).filter(
                trainess__in=UserProfile.objects.filter(
                    is_student=True).filter(score='1')))

        data['statistic_by_course'] = statistic_by_course
        statistic_by_gender = UserProfile.objects.filter(is_student=True).values('gender').annotate(
            Count('gender')).order_by('gender')
        data['statistic_by_gender'] = statistic_by_gender
        statistic_by_gender_for_approved = UserProfile.objects.filter(is_student=True).filter(
            trainesscourserecord__approved__in=[True]).filter(
            trainesscourserecord__trainess_approved__in=[True]).values('gender').annotate(Count('gender')).order_by(
            'gender')
        data['statistic_by_gender_for_approved'] = statistic_by_gender_for_approved
        log.debug(statistic_by_gender, extra=d)
        statistic_by_university = UserProfile.objects.filter(is_student=True).values('university').annotate(
            Count('university')).order_by('-university__count')
        data['statistic_by_university'] = statistic_by_university

        statistic_by_university_for_approved = UserProfile.objects.filter(is_student=True).values('university').filter(
            trainesscourserecord__approved__in=[True]).filter(
            trainesscourserecord__trainess_approved__in=[True]).annotate(Count('university')).order_by(
            '-university__count')
        data['statistic_by_university_for_approved'] = statistic_by_university_for_approved

        # kurs bazinda toplam teyitli olanlar
        data['statistic_by_course_for_apply'] = TrainessCourseRecord.objects.filter(trainess_approved=True).values(
            'course__name').annotate(count=Count('course')).order_by('-count')
        total_profile = len(UserProfile.objects.filter(is_student=True))
        total_preference = len(TrainessCourseRecord.objects.all())
        total_preference_for_approved = len(
            TrainessCourseRecord.objects.filter(approved=True).filter(trainess_approved=True))
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
            trainess_course_records = TrainessCourseRecord.objects.filter(trainess=userprofile)
            context = {}
            approvedpref = None
            for tcr in trainess_course_records:
                try:
                    # x. tercih onaylama donemi baslangic zamani ile x. tercih teyit etme donemi arasinda ise mail atsin.
                    if tcr.approved:
                        approvedpref = tcr
                    if data['site'].application_end_date < now_for_approve < data['site'].event_start_date:
                        if tcr.trainess_approved:
                            context['trainess_course_record'] = tcr
                            send_email("training/messages/notice_for_canceled_courses_subject.html",
                                       "training/messages/notice_for_canceled_courses.html",
                                       "training/messages/notice_for_canceled_courses.text",
                                       context,
                                       EMAIL_FROM_ADDRESS,
                                       tcr.course.trainer.all().values_list('user__username', flat=True))
                except Exception as e:
                    log.error(e.message, extra=d)
                trainess_course_records.delete()
            if data['site'].application_end_date < datetime.date(now_for_approve):
                remaining_days = int((data['site'].event_start_date - datetime.date(now_for_approve)).days)
                notestr = "Kursların başlamasına %d gun kala tüm başvurularını iptal etti." % remaining_days
                if approvedpref:
                    # Kullanicinin tercihi kursa kaç gün kala kabul görmüş
                    daysbetweenapproveandevent = int((data['site'].event_start_date - approvedpref.instapprovedate).days)
                    notestr += "\nTercihi kursun başlamasına %d gün kala kabul edilmiş." % daysbetweenapproveandevent
            else:
                notestr = "Kullanici tercihlerini iptal etti"
            if cancelnote:
                notestr += "\nİptal Sebebi:%s" % cancelnote
            if notestr:
                note = TrainessNote(note=notestr, note_from_profile=userprofile, note_to_profile=userprofile,
                                    site=data['site'], note_date=now_for_approve)
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
            course_records = TrainessCourseRecord.objects.filter(trainess__user=request.user).order_by(
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
    log.debug(request)
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    if request.method == "POST":
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect("createprofile")
        TrainessCourseRecord.objects.filter(trainess=userprofile).delete()
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


@staff_member_required
def participationstatuses(request):
    """
    Admin veya is_staff yetkisi verilmiş başka bir kullanıcı ile buraya view ile yoklama kaydı girilecek.
    :param request: HttpRequest
    """
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    data['allcourses'] = Course.objects.filter(site=data['site'].pk)
    data['note'] = "İşlem yapmak istediğiniz kursu seçiniz."
    return render_to_response('training/participationstatuses.html', data, context_instance=RequestContext(request))


@staff_member_required
def editparticipationstatusebycourse(request, courseid):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    data['courserecords'] = TrainessCourseRecord.objects.filter(course=courseid, approved=True, trainess_approved=True)
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
