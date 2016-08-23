# -*- coding:utf-8  -*-
import sys
import json
import logging
import datetime

from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login
from django.contrib.auth import logout as logout_user
from django.template import RequestContext

from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required

from userprofile.forms import CreateUserForm, UpdateUserForm, StuProfileForm, InstructorInformationForm, \
    ChangePasswordForm, UserProfileBySiteForm, UserProfileBySiteForStaffForm
from userprofile.models import Accommodation, UserProfile, UserAccomodationPref, InstructorInformation, \
    UserVerification, TrainessNote, TrainessClassicTestAnswers, UserProfileBySite
from userprofile.userprofileops import UserProfileOPS
from userprofile.uutils import getuserprofileforms

from training.tutils import getparticipationforms, cancel_all_prefs

from training.models import Course, TrainessCourseRecord, TrainessParticipation

from abkayit.models import *
from abkayit.backend import getsiteandmenus, create_verification_link, send_email_by_operation_name

from abkayit.decorators import active_required

from abkayit.settings import ACCOMODATION_PREFERENCE_LIMIT

log = logging.getLogger(__name__)


def subscribe(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    data = getsiteandmenus(request)
    if not request.user.is_authenticated():
        note = _("Register to system to participate in courses before the conferences")
        form = CreateUserForm()
        if 'register' in request.POST:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save(commit=True)
                    user.set_password(user.password)
                    try:
                        user.save()
                        note = _("Your account has been created. Please check your email for activation link")
                    except Exception as e:
                        note = e.message
                    form = None
                except Exception as e:
                    note = _("Your account couldn't create. Please try again!")
                    log.error(e.message, extra=d)
        elif 'cancel' in request.POST:
            return redirect("subscribe")
        data['createuserform'] = form
        data['note'] = note
        return render_to_response("userprofile/subscription.html", data, context_instance=RequestContext(request))
    else:
        return redirect("selectcoursefcp")


@login_required(login_url='/')
def getaccomodations(request, usertype, gender):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    log.info("getaccomodation funtion call", extra=d)
    data = getsiteandmenus(request)
    jsondata = {}
    accomodations = Accommodation.objects.filter(
        usertype__in=[usertype, 'hepsi']).filter(
        gender__in=[gender, 'H']).filter(
        site=data['site']).values_list('id', 'name').order_by('name')
    for a in accomodations:
        jsondata[a[0]] = a[1]
    return HttpResponse(json.dumps(jsondata), content_type="application/json")


@login_required(login_url='/')
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def createprofile(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    data = getsiteandmenus(request)
    log.info("create/update profile form", extra=d)
    data['update_user_form'] = UpdateUserForm(instance=request.user)
    data['note'] = "Profilinizi güncelleyebilirsiniz."
    note, userprobysite, data['userproform'], data['userproformbysite'], data['accomodations'], data[
        'accomodation_records'] = getuserprofileforms(request.user, data['site'], d)
    data['sitewidequestions'] = TextBoxQuestions.objects.filter(site=data["site"], active=True, is_sitewide=True)
    if 'register' in request.POST:
        data['update_user_form'] = UpdateUserForm(data=request.POST, instance=request.user)
        try:
            data['userproform'] = StuProfileForm(request.POST, request.FILES, instance=request.user.userprofile,
                                                 ruser=request.user)
        except UserProfile.DoesNotExist:
            data['userproform'] = StuProfileForm(request.POST, request.FILES, ruser=request.user)
        if data['site'].needs_document:
            if userprobysite:
                data['userproformbysite'] = UserProfileBySiteForm(request.POST, request.FILES, instance=userprobysite,
                                                                  ruser=request.user, site=data['site'])
            else:
                data['userproformbysite'] = UserProfileBySiteForm(request.POST, request.FILES, ruser=request.user,
                                                                  site=data['site'])
        if data['update_user_form'].is_valid():
            data['update_user_form'].save()
            if data['userproform'].is_valid():
                try:
                    data['userproform'].save()
                    if data['sitewidequestions']:
                        for question in data['sitewidequestions']:
                            answer = request.POST.get("answer%s" % question.pk, "")
                            if answer:
                                tca, created = TrainessClassicTestAnswers.objects.get_or_create(
                                    user=request.user.userprofile, question=question)
                                tca.answer = answer
                                tca.save()
                    if not UserProfileOPS.is_instructor(request.user.userprofile) and ACCOMODATION_PREFERENCE_LIMIT:
                        prefs = UserAccomodationPref.objects.filter(user=request.user.userprofile)
                        if prefs:
                            prefs.delete()
                        if 'tercih1' in request.POST.keys():
                            try:
                                uaccpref = UserAccomodationPref(user=request.user.userprofile,
                                                                accomodation=Accommodation.objects.get(
                                                                    pk=request.POST.get('tercih1')),
                                                                usertype="stu", preference_order=1)
                                uaccpref.save()
                                log.info("Kullanıcı profilini ve konaklama tercihini güncelledi.", extra=d)
                                if data['site'].needs_document:
                                    if data['userproformbysite'].is_valid():
                                        data['userproformbysite'].save()
                                        if 'document' in request.FILES:
                                            log.info("Kullanıcı evrakını güncelledi.", extra=d)
                                    else:
                                        data['note'] = "Profiliniz aşağıdaki sebeplerden dolayı kaydedilemedi"
                                        return render_to_response("userprofile/user_profile.html", data,
                                                                  context_instance=RequestContext(request))
                            except Exception as e:
                                log.error(e.message, extra=d)
                                data['note'] = "Profiliniz kaydedildi ancak konaklama tercihleriniz kaydedilemedi." \
                                               " Sistem yöneticisi ile görüşün!"
                                return render_to_response("userprofile/user_profile.html", data,
                                                          context_instance=RequestContext(request))
                    data['note'] = "Profiliniz başarılı bir şekilde kaydedildi. Kurs tercihleri adımından" \
                                   " devam edebilirsiniz"
                    return render_to_response("userprofile/user_profile.html", data,
                                              context_instance=RequestContext(request))
                except Exception as e:
                    log.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), extra=d)
                    log.error(e.message, extra=d)
                    data['note'] = "Profiliniz kaydedilirken hata oluştu lütfen sayfayı yeniden yükleyip tekrar deneyin"
                    return render_to_response("userprofile/user_profile.html", data,
                                              context_instance=RequestContext(request))
        data['note'] = "Profiliniz aşağıdaki sebeplerden dolayı oluşturulamadı"
    elif 'cancel' in request.POST:
        return redirect("createprofile")
    return render_to_response("userprofile/user_profile.html", data, context_instance=RequestContext(request))


@login_required(login_url='/')
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def instructor_information_view(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    if not request.user.userprofile:
        log.error("Kullanıcı Profili Bulunamadı", extra=d)
        return redirect("createprofile")
    data = getsiteandmenus(request)
    if not UserProfileOPS.is_instructor(request.user.userprofile):
        note = _("You are not authorized to access here")
    else:
        note = _("Please enter your transformation, arrival date, departure date information")
        try:
            instructorinformation = InstructorInformation.objects.get(user=request.user.userprofile, site=data['site'])
            form = InstructorInformationForm(instance=instructorinformation, site=data['site'], request=request)

        except ObjectDoesNotExist as e:
            log.debug("Egitmen bilgileri bulunamadi, yeni bilgiler olusturulmak icin form acilacak", extra=d)
            log.error(e.message, extra=d)
            form = InstructorInformationForm(site=data['site'], request=request)
            instructorinformation = None

        if request.POST:
            if instructorinformation is not None:
                form = InstructorInformationForm(request.POST, instance=instructorinformation, site=data['site'],
                                                 request=request)
            else:
                form = InstructorInformationForm(request.POST, site=data['site'], request=request)
            if form.is_valid():
                try:
                    instructor_info = form.save(commit=True)
                    note = _("Your information saved successfully")
                    log.info("%s egitmeni ek bilgilerini guncelledi" % instructor_info.user.user.username, extra=d)
                except Exception as e:
                    note = _("An error occurred while saving your information")
                    log.error(e.message, extra=d)
        data['form'] = form
    data['note'] = note
    return render_to_response("userprofile/instructor_information.html", data, context_instance=RequestContext(request))


@staff_member_required
def alluserview(request):
    """
    Kabul edilen tüm kullanıcıların konaklama bilgileri
    :param request:
    :return:
    """
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    data = getsiteandmenus(request)
    userlist = []
    try:
        allcourserecord = TrainessCourseRecord.objects.filter(course__site__is_active=True).values_list(
            'trainess').order_by('trainess').distinct()
        if allcourserecord:

            for r in allcourserecord:
                up = UserProfile.objects.get(pk=r[0])
                usr = {
                    "pk": up.pk,
                    "firstname": up.user.first_name,
                    "email": up.user.username, "lastname": up.user.last_name,
                    "tcino": up.tckimlikno if up.tckimlikno != '' else up.ykimlikno,
                    "university": up.university,
                    "gender": up.gender,
                    "job": up.job,
                    "title": up.title,
                    "accomodation": up.useraccomodationpref_set.filter(accomodation__site__is_active=True),
                    "courserecordid": "0"}
                try:
                    usr['document'] = up.userprofilebysite.document
                    usr['needs_document'] = up.userprofilebysite.needs_document
                except:
                    usr['document'] = None
                    usr['needs_document'] = False
                userlist.append(usr)
    except Exception as e:
        log.error("An error occured while showing alluserview", extra=d)
        log.error(e.message, extra=d)
    log.info("All user view showed", extra=d)
    data["datalist"] = userlist
    return render_to_response("userprofile/allusers.html", data, context_instance=RequestContext(request))


@staff_member_required
def get_all_trainers_view(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    data = getsiteandmenus(request)
    try:
        trainers = []
        courses = Course.objects.filter(site__is_active=True)
        for course in courses:
            trainers.extend(course.trainer.all())
        data['trainers'] = set(trainers)
    except Exception as e:
        log.error(e.message, extra=d)
    return render_to_response("userprofile/alltrainers.html", data, context_instance=RequestContext(request))


def active(request, key):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    try:
        user_verification = UserVerification.objects.get(activation_key=key)
        user = user_verification.user
        user.is_active = True
        user.save()
        backend_login(request, user)
    except ObjectDoesNotExist as e:
        log.error(e.message, extra=d)
    except Exception as e:
        log.error(e.message, extra=d)
    return redirect("createprofile")


def active_resend(request):
    data = getsiteandmenus(request)
    note = _("Please activate your account.  If you want to re-send an activation email, please click following button")
    if request.POST:
        domain = data['site'].home_url
        data['domain'] = domain.rstrip('/')
        user_verification, created = UserVerification.objects.get_or_create(user=request.user)
        user_verification.activation_key = create_verification_link(request.user)
        user_verification.save()
        data['activation_key'] = user_verification.activation_key
        data['recipientlist'] = [request.user.username]
        note = send_email_by_operation_name(data, "send_activation_key")
    data['note'] = note
    return render_to_response("userprofile/activate_resend.html", data, context_instance=RequestContext(request))


@login_required(login_url='/')
def password_reset(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    data = getsiteandmenus(request)
    form = ChangePasswordForm()
    note = _("Change your password")
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                request.user.set_password(form.cleaned_data['password'])
                request.user.save()
                backend_login(request, request.user)
                note = _("""Your password has been changed""")
                form = None
            except Exception as e:
                note = _("""Your password couldn't be changed""")
                log.error(e.message, extra=d)
    data['changepasswordform'] = form
    data['note'] = note
    return render_to_response("userprofile/change_password.html", data, context_instance=RequestContext(request))


def password_reset_key(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    data = getsiteandmenus(request)
    note = _("Please enter your registered email")
    if request.method == 'POST':
        email = request.POST['email']
        if email and email != "":
            try:
                user = User.objects.get(username=request.POST['email'])
                user_verification, created = UserVerification.objects.get_or_create(user=user)
                user_verification.password_reset_key = create_verification_link(user)
                user_verification.save()
                data['ruser'] = user
                data['activation_key'] = user_verification.password_reset_key
                domain = data['site'].home_url
                data['domain'] = domain.rstrip('/')
                data['recipientlist'] = [user.username]
                note = send_email_by_operation_name(data, "send_reset_password_key")
                if note:
                    note = "Parola sıfırlama e-postası adresinize gönderildi."
                else:
                    note = "E-posta gönderilemedi"
            except ObjectDoesNotExist:
                note = _("""There isn't any user record with this e-mail on the system""")
                log.error(note, extra=d)
            except Exception as e:
                note = _("""Password reset operation failed""")
                log.error(note, extra=d)
                log.error(e.message, extra=d)
        else:
            note = _("""Email field can not be empty""")
            log.error(note, extra=d)
    data['note'] = note
    return render_to_response("userprofile/change_password_key_request.html", data,
                              context_instance=RequestContext(request))


def password_reset_key_done(request, key=None):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    data = getsiteandmenus(request)
    form = ChangePasswordForm()
    note = _("Change your password")
    try:
        user_verification = UserVerification.objects.get(password_reset_key=key)
        user = user_verification.user
        user.is_authenticated = False
        user.save()
        request.user = user
    except Exception as e:
        note = _("""Password reset operation failed""")
        log.error(e.message, extra=d)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                request.user.set_password(form.cleaned_data['password'])
                request.user.save()
                note = _("""Your password has been changed""")
                form = None
                redirect("index")
            except Exception as e:
                note = _("""Your password couldn't be changed""")
                log.error(e.message, extra=d)
    data['changepasswordform'] = form
    data['note'] = note
    data['user'] = request.user
    return render_to_response("userprofile/change_password.html", data, context_instance=RequestContext(request))


@login_required(login_url='/')
def save_note(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    data = getsiteandmenus(request)
    jsondata = {}
    if request.method == 'POST':
        trainess_username = request.POST['trainess_username']
        t_note = request.POST['note']
        if trainess_username and trainess_username != '':
            try:
                userprofile = UserProfile.objects.get(user__username=trainess_username)
                trainess_note = TrainessNote.objects.create(note_to_profile=userprofile, site=data['site'])
                trainess_note.label = "kurs"
                trainess_note.note = t_note
                trainess_note.note_from_profile = request.user.userprofile
                trainess_note.note_date = datetime.now()
                trainess_note.save()
                jsondata['status'] = "0"
                jsondata['message'] = "Durum güncellendi!"
            except Exception as e:
                jsondata['status'] = "-1"
                jsondata['message'] = "Durum güncelleme sırasında hata olustu"
                log.error(e.message, extra=d)
        else:
            jsondata['status'] = "-1"
            jsondata['message'] = "Hata: Kullanıcı adı boş olamaz!"
            log.error("username bos olamaz", extra=d)

    return HttpResponse(json.dumps(jsondata), content_type="application/json")


def logout(request):
    logout_user(request)
    return HttpResponseRedirect("/")


def backend_login(request, user):
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)


@login_required
def showuserprofile(request, userid, courserecordid):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}  # d: bu degiskeni loglarda kullanıyoruz
    data = getsiteandmenus(request)
    if UserProfileOPS.is_instructor(request.user.userprofile) or request.user.is_staff:
        courserecord = None
        try:
            courserecord = TrainessCourseRecord.objects.get(pk=courserecordid,
                                                            trainess=UserProfile.objects.get(pk=userid))
            if not request.user.is_staff and request.user.userprofile not in courserecord.course.trainer.all() and \
                            request.user.userprofile not in courserecord.course.authorized_trainer.all():
                return redirect("selectcoursefcp")
        except Exception as e:
            log.warning(e.message, extra=d)
            log.warning("Staff user show user profile", extra=d)
            if not request.user.is_staff:
                return redirect("selectcoursefcp")
        user = UserProfile.objects.get(pk=userid)
        data['tuser'] = user
        data['ruser'] = request.user
        data['note'] = "Detaylı kullanıcı bilgileri"
        if user:
            userprofilebysite = None
            try:
                userprofilebysite = UserProfileBySite.objects.get(user=user.user)
                data['userprofilebysiteform'] = UserProfileBySiteForStaffForm(instance=userprofilebysite,
                                                                              ruser=request.user, site=data['site'],
                                                                              user=user.user)
            except UserProfileBySite.DoesNotExist as e:
                data['userprofilebysiteform'] = UserProfileBySiteForStaffForm(ruser=request.user, site=data['site'],
                                                                              user=user.user)
            if "savesitebasedprofile" in request.POST:
                if userprofilebysite:
                    data['userprofilebysiteform'] = UserProfileBySiteForStaffForm(request.POST, request.FILES,
                                                                                  instance=userprofilebysite,
                                                                                  ruser=request.user, site=data['site'],
                                                                                  user=user.user)
                else:
                    data['userprofilebysiteform'] = UserProfileBySiteForStaffForm(request.POST, request.FILES,
                                                                                  ruser=request.user, site=data['site'],
                                                                                  user=user.user)
                if data['userprofilebysiteform'].is_valid():
                    data['userprofilebysiteform'].save()
                    log.info("%s kullanıcısı için etkinlik bazlı profil kaydedildi", extra=d)
                    data['note'] = "Etkinlik bazlı profil kaydedildi."
                else:
                    data['note'] = "Kullanici bazlı profil formu doğrulanamadı."
            if request.user.is_staff and "cancelall" in request.POST:
                cancelnote = request.POST.get('trainesscancelnotetext', '')
                res = cancel_all_prefs(user, cancelnote, data['site'], request.user, d)
                if res == 1:
                    data['note'] = "Kullanıcının Tüm Başvuruları Silindi"
                else:
                    data['note'] = "Kullanıcının Başvuruları silinirken hata oluştu"
            if courserecord:
                data['courseid'] = courserecord.course.pk
                if request.user.is_staff and courserecord.consentemailsent:
                    try:
                        data['forms'] = getparticipationforms(data['site'], courserecord)
                        if "save" in request.POST:
                            for date in range(1, int(
                                    (data['site'].event_end_date - data['site'].event_start_date).days) + 1):
                                morning = request.POST.get("participation" + str(date) + "-morning")
                                afternoon = request.POST.get("participation" + str(date) + "-afternoon")
                                evening = request.POST.get("participation" + str(date) + "-evening")
                                data['note'] = 'Seçimleriniz başarıyla kaydedildi.'
                                log.info("%s nolu kurs kaydinin yoklama kaydi girişi başarılı" % courserecord.pk,
                                         extra=d)
                                try:
                                    tp = TrainessParticipation.objects.get(courserecord=courserecord, day=str(date))
                                    tp.morning = morning
                                    tp.afternoon = afternoon
                                    tp.evening = evening
                                    tp.save()
                                except ObjectDoesNotExist as e:
                                    tp = TrainessParticipation(courserecord=courserecord, day=str(date),
                                                               morning=morning, afternoon=afternoon, evening=evening)
                                    tp.save()
                                except:
                                    data['note'] = 'Hata oluştu!'
                                    log.info("%s nolu kurs kaydinin yoklama kaydi girişi hatalı" % courserecord.pk,
                                             extra=d)
                                data['forms'] = getparticipationforms(data['site'], courserecord)
                    except Exception as e:
                        log.error(e.message, extra=d)
        else:
            data['note'] = "Böyle Bir kullanıcı yoktur."
        return render_to_response("userprofile/showuserprofile.html", data, context_instance=RequestContext(request))
    return redirect("selectcoursefcp")
