# -*- coding: utf-8 -*-
import sys
import json
import logging
import itertools
from datetime import datetime

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone

from abkayit.models import ApprovalDate, Answer
from abkayit.decorators import active_required
from abkayit.settings import PREFERENCE_LIMIT, ADDITION_PREFERENCE_LIMIT, REQUIRE_TRAINESS_APPROVE, \
    UNIVERSITIES

from userprofile.models import UserProfile, TrainessNote, TrainessClassicTestAnswers, UserProfileBySite
from userprofile.forms import InstProfileForm, CreateInstForm
from userprofile.userprofileops import UserProfileOPS

from training.models import Course, TrainessCourseRecord, TrainessParticipation
from training.forms import CreateCourseForm, AddTrainessForm
from training.tutils import get_approve_start_end_dates_for_inst, save_course_prefferences, applytrainerselections
from training.tutils import get_additional_pref_start_end_dates_for_trainess
from training.tutils import get_approved_trainess, get_trainess_by_course, is_trainess_approved_any_course, \
    gettestsofcourses, cancel_all_prefs, get_approve_first_start_last_end_dates_for_inst, daterange, \
    getparticipationforms_by_date, calculate_participations

log = logging.getLogger(__name__)

DATETIME_FORMAT = "%d/%m/%Y %H:%M"


@login_required
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def show_course(request, course_id):
    try:
        data = {}
        course = Course.objects.get(id=course_id)
        data['course'] = course
        return render(request, 'training/course_detail.html', data)
    except ObjectDoesNotExist:
        return HttpResponse("Kurs Bulunamadi")


@login_required
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def list_courses(request):
    data = {}
    courses = Course.objects.filter(site=request.site)
    data['courses'] = courses
    return render(request, 'training/courses.html', data)


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
    data = {'closed': True, 'additional1_pref_closed': True, 'PREFERENCE_LIMIT': PREFERENCE_LIMIT,
            'ADDITION_PREFERENCE_LIMIT': ADDITION_PREFERENCE_LIMIT}
    now = datetime.now()
    data['may_cancel_all'] = True if request.site.event_start_date > datetime.date(now) else False
    """
    courses: mevcut etkinte onaylanmis ve basvuruya acik kurslar
    """
    data['courses'] = Course.objects.filter(approved=True, site=request.site, application_is_open=True)
    """
    course_records: katilimcinin, mevcut etkinlikteki tercihleri
    """
    data['course_records'] = TrainessCourseRecord.objects.filter(trainess__user=request.user,
                                                                 course__site=request.site).order_by(
            'preference_order')
    userprofile = request.user.userprofile
    if not userprofile:
        log.info("userprofile not found", extra=request.log_extra)
        return redirect("createprofile")
    if data['courses']:
        if request.site.application_start_date <= datetime.date(now) <= request.site.application_end_date:
            log.info("in between application start and end date", extra=request.log_extra)
            ubysite, created = UserProfileBySite.objects.get_or_create(site=request.site, user=request.user)
            if ubysite.userpassedtest:
                data['closed'] = False
                data['note '] = _("You can choose courses in order of preference.")
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
                                        return render(request, "training/testforapplication.html", data)
                                for question in questions[1]:
                                    tbansw = request.POST.get("answer" + str(question.pk))
                                    if tbansw:
                                        tcta, created = TrainessClassicTestAnswers.objects.get_or_create(
                                                user=request.user.userprofile, question=question)
                                        tcta.answer = tbansw
                                        tcta.save()
                            res = save_course_prefferences(userprofile, course_prefs, request.site, request.log_extra,
                                                           answersforcourse=answersforcourse)
                            data['note'] = res['message']
                            return render(request, "training/applytocourse.html", data)
                        return render(request, "training/testforapplication.html", data)
                    else:
                        res = save_course_prefferences(userprofile, course_prefs, request.site, request.log_extra)
                        data['note'] = res['message']
                    data['note'] = res['message']
                    return render(request, "training/applytocourse.html", data)
            else:
                return redirect("testbeforeapply")
        elif datetime.date(now) < request.site.application_start_date:
            log.info("before application start date", extra=request.log_extra)
            data['note'] = "Tercih dönemi %s tarihinde açılacaktır" % request.site.application_start_date
        elif datetime.date(now) > request.site.application_end_date:
            log.info("after application end date", extra=request.log_extra)
            data[
                'note'] = "Tercih dönemi %s tarihinde kapanmıştır. Başvuru durumunuzu İşlemler> Başvuru Durum/Onayla " \
                          "adımından görüntüleyebilirsiniz " % request.site.application_end_date
            """
             Bu kod parcasi ek tercihler icindir. Eger kullanıcının kabul ettigi ve edildigi bir kurs yoksa ve
             ek tercih aktifse bu kod blogu calisir.
            """
            if ADDITION_PREFERENCE_LIMIT:
                adates = get_additional_pref_start_end_dates_for_trainess(request.site, request.log_extra)
                if adates:
                    for adate in adates:
                        if adates[adate].start_date <= now <= adates[adate].end_date:
                            if is_trainess_approved_any_course(userprofile, request.site, request.log_extra):
                                data['additional1_pref_closed'] = False
                                log.info("ek tercih aktif", extra=request.log_extra)
                                data['note'] = _("You can make additional preference.")
    else:
        data['note'] = _("There isn't any course in this event.")
    return render(request, 'training/applytocourse.html', data)


@login_required
def testforapplication(request):
    data = {}

    return render(request, "training/testforapplication.html", data)


@login_required
def approve_course_preference(request):
    """
    Bu view katilimci bir kursa kabul edilip edilmedigini görüntülemesi ve katilimcidan katılıp katılmayacağına dair
    son bir teyit alınır.
    :param request: HttpRequest
    :return:
    """
    message = ""
    status = "1"
    data = {"note": "Başvuru Durumunuz"}
    now = datetime.now()
    try:

        data["approve_is_open"] = False
        trainess_course_records = TrainessCourseRecord.objects.filter(trainess=request.user.userprofile,
                                                                      course__site=request.site)
        first_start_date_inst, last_end_date_inst = get_approve_first_start_last_end_dates_for_inst(request.site,
                                                                                                    request.log_extra)
        if not trainess_course_records:
            data['note'] = "Henüz herhangi bir kursa başvuru yapmadınız!"
        elif request.site.application_start_date <= datetime.date(now) < request.site.application_end_date:
            data['note'] = "Başvurunuz için teşekkürler. Değerlendirme sürecinin başlaması için " \
                           "tüm başvuruların tamamlanması beklenmektedir."
        else:
            recordapprovedbyinst = TrainessCourseRecord.objects.filter(trainess=request.user.userprofile, approved=True,
                                                                       consentemailsent=True,
                                                                       course__site=request.site)
            if not recordapprovedbyinst:

                if first_start_date_inst.start_date <= now < last_end_date_inst.end_date:
                    data['note'] = "Başvurular değerlendirilmektedir. En geç %s tarihine kadar sonuçları burada" \
                                   " görebilirsiniz." % last_end_date_inst.end_date.strftime("%d-%m-%Y")
                elif request.site.event_start_date - 1 > now > last_end_date_inst.end_date:
                    data['note'] = "Kurslara kabul dönemi bitmiş olup başvurularınıza kabul edilmediniz ancak" \
                                   " kurs başlangıç tarihine kadar kabul edilme şansınız hala devam ediyor." \
                                   " Takip etmeye devam edin."
                elif request.site.event_start_date - 1 <= now:
                    data['note'] = "Başvurularınız kabul edilmemiştir. Bir sonraki etkinlikte görüşmek dileğiyle."
            else:
                data["note"] = "Aşağıdaki Kursa Kabul Edildiniz"
                data['trainess_course_record'] = recordapprovedbyinst[0]
                if REQUIRE_TRAINESS_APPROVE:
                    recordapprovedbytra = recordapprovedbyinst.filter(trainess_approved=True)
                    if not recordapprovedbytra:
                        tra_approvaldate = ApprovalDate.objects.get(site=request.site, for_trainess=True,
                                                                    preference_order=recordapprovedbyinst[
                                                                        0].preference_order)
                        if tra_approvaldate.start_date <= now <= tra_approvaldate.end_date:
                            data['note'] = "Aşağıdaki kursa kabul edildiniz"
                            data["approve_is_open"] = True
                        else:
                            data[
                                "note"] = "Aşağıdaki kursa kabul edildiniz ancak teyit etmediniz. Kursa katılamazsınız."
                            data["approve_is_open"] = False
    except Exception as e:
        log.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), extra=request.log_extra)
        log.error(e.message, extra=request.log_extra)
        data['note'] = "Hata oluştu"
    if request.POST:
        try:
            log.debug(request.POST.get("courseRecordId"), extra=request.log_extra)
            if request.POST.get("courseRecordId") and data['trainess_course_record']:
                data['trainess_course_record'].trainess_approved = True
                data['trainess_course_record'].save()
                message = "İşleminiz başarılı bir şekilde gerçekleştirildi"
                status = "0"
                log.debug("kursu onayladi " + data['trainess_course_record'].course.name, extra=request.log_extra)
        except Exception as e:
            log.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), extra=request.log_extra)
            log.error(e.message, extra=request.log_extra)
            message = "İşleminiz Sırasında Hata Oluştu"
            status = "-1"
        return HttpResponse(json.dumps({'status': status, 'message': message}), content_type="application/json")
    return render(request, "training/confirm_course_preference.html", data)

@login_required
def view_pdf(request, rid):
    path = "/opt/ab-kurs-kayit/abkayit/mektuplar/Kurslar/%s.pdf" % (str(rid))
    tcr = TrainessCourseRecord.objects.filter(pk=rid, consentemailsent=True).first()
    if tcr:
        if request.user == tcr.trainess.user:
            with open(path, 'r') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline;filename=some_file.pdf'
                return response
            pdf.closed
    return HttpResponse("yetkiniz yok.")

@login_required
def control_panel(request, courseid):
    data = {'note': _("You can accept trainees")}
    now = timezone.now()
    try:
        course = Course.objects.get(pk=courseid)
        data['now'] = now
        data['user'] = request.user
        data['dates'] = get_approve_start_end_dates_for_inst(request.site, request.log_extra)
        data['trainess'] = {}
        data['notesavedsuccessful'] = False
        if data['dates']:
            if now <= data['dates'].get(1).end_date:
                data['trainess'][course] = get_trainess_by_course(course, request.log_extra)
            else:
                data['note'] = _("Consent period is closed")
                data['trainess'][course] = get_approved_trainess(course, request.log_extra)
        if request.user.userprofile in course.authorized_trainer.all():
            log.info("Kullanıcı %s kursunda degisiklik yapiyor" % course.name, extra=request.log_extra)
            if "send" in request.POST:
                log.info("kursiyer onay islemi basladi", extra=request.log_extra)
                log.info(request.POST, extra=request.log_extra)
                data['note'] = applytrainerselections(request.POST, course, data, request.site, request.log_extra)
            return render(request, "training/controlpanel.html", data)
        elif request.user.userprofile in course.trainer.all():
            data['note'] = "Kursiyerler için not ekleyebilirsiniz."
            if "savescore" in request.POST:
                trainessnote = request.POST.get('trainessnotetext')
                trainessusername = request.POST.get('trainessnoteuser')
                user = User.objects.get(username=trainessusername)
                data['note'] = UserProfileOPS.savenote(request, user, trainessnote)
                potentialinst = request.POST.get('potential-%s' % user.pk)
                uprobysite, created = UserProfileBySite.objects.get_or_create(user=user, site=request.site)
                if potentialinst == 'on':
                    uprobysite.potentialinstructor = True
                else:
                    uprobysite.potentialinstructor = False
                uprobysite.save()
                data['savednoteuserid'] = user.userprofile.pk
                data['notesavedsuccessful'] = True
            return render(request, "training/controlpanelforunauthinst.html", data)
        elif not request.user.is_staff:
            return redirect("applytocourse")
        return redirect("statistic")
    except UserProfile.DoesNotExist:
        return redirect("createprofile")


@login_required
def select_course_for_control_panel(request):
    data = {'note': "İşlem Yapmak İstediğiniz Kursu Seçiniz", 'user': request.user}
    try:
        if UserProfileOPS.is_instructor(request.user.userprofile):
            courses = Course.objects.filter(site=request.site, approved=True, trainer__user=request.user)
            if courses:
                log.info("egitmenin " + str(len(courses)) + " tane kursu var", extra=request.log_extra)
                data['courses'] = courses
            else:
                data['note'] = "Bu etkinlikte kursunuz yok."
            return render(request, "training/courselistforinst.html", data)
        elif not request.user.is_staff:
            return redirect("applytocourse")
        return redirect("statistic")
    except UserProfile.DoesNotExist:
        return redirect("createprofile")


@staff_member_required
def allcourseprefview(request):
    data = {}
    data['datalist'] = TrainessCourseRecord.objects.filter(course__site=request.site)
    return render(request, "training/allcourseprefs.html", data)


@staff_member_required
def allapprovedprefsview(request):
    data = {}
    data['datalist'] = TrainessCourseRecord.objects.filter(course__site=request.site, approved=True)
    data['participations'] = {}
    for tcr in data['datalist']:
        tprs = TrainessParticipation.objects.filter(
                courserecord=tcr)  # Bir katilimcinin bu tercihi icin yoklama kayitlari
        if tprs:
            totalparticipation, totalcoursehour = calculate_participations(tprs, request.site)
            data['participations'][tcr] = "%s saatlik kursun %s lik kısmına katildi" % (
                totalcoursehour, totalparticipation)
        else:
            data['participations'][tcr] = "Bu kisinin yoklama kaydi yok"

    return render(request, "training/allapprovedprefs.html", data)


def statistic(request):
    if request.user.is_staff or UserProfileOPS.is_instructor(request.user.userprofile):
        data = {}
        try:
            record_data = TrainessCourseRecord.objects.filter(course__site=request.site).values(
                    'course', 'preference_order').annotate(
                    Count('preference_order')).order_by(
                    'course', '-preference_order')
            statistic_by_course = {}
            for key, group in itertools.groupby(record_data, lambda item: item["course"]):
                course_object = Course.objects.get(pk=key, site=request.site)
                statistic_by_course[course_object] = {str(item['preference_order']): item['preference_order__count'] for
                                                      item in group}
                statistic_by_course[course_object]['total_apply'] = len(TrainessCourseRecord.objects.filter(
                        course=course_object))
                statistic_by_course[course_object]['total_apply_by_trainer'] = len(TrainessCourseRecord.objects.filter(
                        course=course_object, approved=True))
                statistic_by_course[course_object]['applicationbywomen'] = len(
                        TrainessCourseRecord.objects.filter(course=course_object, trainess__gender="K").order_by(
                                "trainess").values_list("trainess").distinct())
                statistic_by_course[course_object]['applicationbymen'] = len(
                        TrainessCourseRecord.objects.filter(course=course_object, trainess__gender="E").order_by(
                                "trainess").values_list("trainess").distinct())
            data['statistic_by_course'] = statistic_by_course

            data['statistic_by_gender_k'] = len(
                    TrainessCourseRecord.objects.filter(course__site=request.site, trainess__gender="K").order_by(
                            "trainess").values_list("trainess").distinct())
            data['statistic_by_gender_e'] = len(
                    TrainessCourseRecord.objects.filter(course__site=request.site, trainess__gender="E").order_by(
                            "trainess").values_list("trainess").distinct())
            data['statistic_by_gender_k_approved'] = len(
                    TrainessCourseRecord.objects.filter(course__site=request.site, trainess__gender="K",
                                                        approved=True).order_by("trainess").values_list(
                            "trainess").distinct())
            data['statistic_by_gender_e_approved'] = len(
                    TrainessCourseRecord.objects.filter(course__site=request.site, trainess__gender="E",
                                                        approved=True).order_by("trainess").values_list(
                            "trainess").distinct())
            data['statistic_by_university'] = TrainessCourseRecord.objects.filter(course__site=request.site).order_by(
                "-trainess__id__count").values("trainess__university").annotate(Count("trainess__university"),
                                                                                Count("trainess__id", distinct=True))

            data['statistic_by_university_for_approved'] = TrainessCourseRecord.objects.filter(
                course__site=request.site, approved=True).order_by("-trainess__id__count").values("trainess__university").annotate(
                Count("trainess__university"), Count("trainess__id", distinct=True))

            data['statistic_by_city'] = TrainessCourseRecord.objects.filter(course__site=request.site).order_by(
                "-trainess__id__count").values("trainess__city").annotate(Count("trainess__city"),
                                                                                Count("trainess__id", distinct=True))
            data['statistic_by_city_for_approved'] = TrainessCourseRecord.objects.filter(course__site=request.site, approved=True).order_by(
                "-trainess__id__count").values("trainess__city").annotate(Count("trainess__city"),
                                                                          Count("trainess__id", distinct=True))

            # kurs bazinda toplam teyitli olanlar
            total_profile = len(
                    TrainessCourseRecord.objects.filter(course__site=request.site).order_by("trainess").values(
                            "trainess").distinct())
            total_preference = len(TrainessCourseRecord.objects.filter(course__site=request.site))
            data['statistic_by_totalsize'] = {'Toplam Profil(Kişi)': total_profile, 'Toplam Tercih': total_preference}
        except Exception as e:
            log.error(e.message, extra=request.log_extra)
        return render(request, "training/statistic.html", data)
    else:
        return redirect("index")


@login_required
def cancel_all_preference(request):
    hres = {'status': '-1', 'message': "Başvurularınız Silinirken Hata Oluştu"}
    if request.POST:
        cancelnote = request.POST.get('cancelnote', '')
        res = cancel_all_prefs(request.user.userprofile, cancelnote, request.site, request.user, request.log_extra)
        if res == 1:
            hres = {'status': '1', 'message': "Tüm Başvurularınız Silindi"}
        else:
            hres = {'status': '-1', 'message': "Başvurularınız silinirken hata oluştu"}
        log.debug(hres['message'], extra=request.log_extra)
    return HttpResponse(json.dumps(hres), content_type="application/json")


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
#            log.error(e.message, extra=request.log_extra)
#        return HttpResponse(json.dumps({'status':'-1', 'message':message}), content_type="application/json")
#    message = "İşleminiz Sırasında Hata Oluştu"
#    return HttpResponse(json.dumps({'status':'-1', 'message':message}), content_type="application/json")


@login_required
def get_preferred_courses(request):
    if request.POST:
        preferred_courses = []
        try:
            course_records = TrainessCourseRecord.objects.filter(course__site=request.site,
                                                                 trainess__user=request.user).order_by(
                'preference_order')
            preferred_courses = [course_record.course.name for course_record in course_records]
            status = "0"
        except Exception as e:
            status = "-1"
            log.error(e.message, extra=request.log_extra)
        return HttpResponse(json.dumps({'status': status, 'preferred_courses': preferred_courses}),
                            content_type="application/json")
    return HttpResponse(json.dumps({'status': '-1'}), content_type="application/json")


@login_required
def apply_course_in_addition(request):
    if request.method == "POST":
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect("createprofile")
        TrainessCourseRecord.objects.filter(course__site=request.site, trainess=userprofile).delete()
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
                            log.debug("ek tercih kaydedildi " + str(course_pre['value']), extra=request.log_extra)
                        else:
                            message = "Kurs basvurulara kapali"
                            log.error(message + " " + str(course_pre['value']), extra=request.log_extra)
                    except Exception as e:
                        log.error(e.message, extra=request.log_extra)
                        message = "Tercihleriniz kaydedilirken hata oluştu"
                        return HttpResponse(json.dumps({'status': '-1', 'message': message}),
                                            content_type="application/json")
                message = "Tercihleriniz başarılı bir şekilde güncellendi"
                return HttpResponse(json.dumps({'status': '0', 'message': message}), content_type="application/json")
    message = "Tercih işlemi yapmanıza izin verilmiyor"
    return HttpResponse(json.dumps({'status': '-1', 'message': message}), content_type="application/json")


@staff_member_required
def addtrainess(request):
    data = {}
    now = datetime.date(datetime.now())
    if UserProfileOPS.is_authorized_inst(
            request.user.userprofile) and request.site.event_start_date > now > request.site.application_end_date:
        data['form'] = AddTrainessForm(request=request)
        data['note'] = "Kursunuza eklemek istediğiniz katilimciyi seçin (E-posta adresine göre)"
        if "add" in request.POST:
            data['form'] = AddTrainessForm(request.POST, request=request)
            if data['form'].is_valid():
                tcourserecord = data['form'].save(commit=False)
                tcourserecord.preference_order = 1
                tcourserecord.trainess_approved = True
                tcourserecord.approved = True
                tcourserecord.save()
                notestr = "Bu kullanicinin %s kursu tercihi eğitmen tarafından eklendi." % tcourserecord.course.name
                tnote = TrainessNote(note=notestr, note_from_profile=request.user.userprofile,
                                     note_to_profile=tcourserecord.trainess,
                                     site=tcourserecord.course.site, note_date=timezone.now(), label="tercih")
                tnote.save()
                data['note'] = "Form kaydedildi. Eklediğiniz katılımcıları 1. tercih listesinde görüntüleyebilirsiniz."
                log.info("%s kullanicisi %s kullanicisini %s kursuna ekledi." % (
                    request.user.username, tcourserecord.trainess.user.username, tcourserecord.course.name),
                         extra=request.log_extra)
            else:
                data['note'] = "Form aşağıdaki sebeplerden dolayı kaydedilemedi."
        elif "cancel" in request.POST:
            return redirect("selectcoursefcp")
        return render(request, 'training/addtrainess.html', data)
    else:
        return redirect("selectcoursefcp")


@staff_member_required
def participationstatuses(request):
    """
    Admin veya is_staff yetkisi verilmiş başka bir kullanıcı ile buraya view ile yoklama kaydı girilecek.
    :param request: HttpRequest
    """
    data = {}
    data['allcourses'] = Course.objects.filter(site=request.site)
    data['daylist'] = list(daterange(request.site.event_start_date, request.site.event_end_date))
    data['note'] = "İşlem yapmak istediğiniz kursu seçiniz."
    return render(request, 'training/participationstatuses.html', data)


@staff_member_required
def editparticipationstatusebycourse(request, courseid, date):
    data = {}
    courserecords = TrainessCourseRecord.objects.filter(course__pk=int(courseid), approved=True)
    data['courserecords'] = {}
    for courserecord in courserecords:
        data['courserecords'][courserecord] = getparticipationforms_by_date(courserecord, date)
    if request.POST:
        for courserecord in courserecords:
            morning = request.POST.get("participation" + str(courserecord.pk) + str(date) + "-morning")
            afternoon = request.POST.get("participation" + str(courserecord.pk) + str(date) + "-afternoon")
            evening = request.POST.get("participation" + str(courserecord.pk) + str(date) + "-evening")
            tp = TrainessParticipation.objects.filter(courserecord=courserecord, day=str(date)).first()
            if tp:
                tp.morning = morning
                tp.afternoon = afternoon
                tp.evening = evening
                tp.save()
            else:
                trainessp = TrainessParticipation(courserecord=courserecord, day=str(date), morning=morning,
                                                  afternoon=afternoon, evening=evening)
                trainessp.save()
            data['courserecords'][courserecord] = getparticipationforms_by_date(courserecord, date)
    data['note'] = "Yoklama bilgilerini girmek için kullanıcı profiline gidiniz."
    data['date'] = date
    return render(request, 'training/courseparstatus.html', data)


@login_required
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def submitandregister(request):
    """
    Bu view'ı kullanmıyoruz. Egitmen ve egitim başvurularını sistemden aldığımızda kullanılabilir.
    :param request:
    :return:
    """
    userops = UserProfileOPS()
    data = {'note': "Kurs onerisi olustur:"}
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
            data['note'] = "Egitim oneriniz basari ile alindi."
        else:
            data['note'] = "Olusturulamadi"
    data['note'] = note
    data['form'] = form
    data['curinstprofform'] = curinstprofform
    data['forms'] = forms
    return render(request, "training/submitandregister.html", data)
