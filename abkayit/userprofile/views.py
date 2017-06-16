# -*- coding:utf-8  -*-
import sys
import json
import logging
from datetime import datetime,timedelta

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import login

from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.tokens import default_token_generator

from userprofile.forms import CreateUserForm, UpdateUserForm, StuProfileForm, InstructorInformationForm, \
    ChangePasswordForm, UserProfileBySiteForm, UserProfileBySiteForStaffForm, ChangePasswordWithSMSForm
from userprofile.models import Accommodation, UserProfile, UserAccomodationPref, InstructorInformation, \
    UserVerification, TrainessNote, TrainessClassicTestAnswers, UserProfileBySite
from userprofile.userprofileops import UserProfileOPS
from userprofile.uutils import getuserprofileforms

from training.tutils import getparticipationforms, cancel_all_prefs

from training.models import Course, TrainessCourseRecord, TrainessParticipation

from abkayit.models import TextBoxQuestions
from abkayit.backend import create_verification_link, send_email_by_operation_name

from abkayit.decorators import active_required

from abkayit.settings import ACCOMODATION_PREFERENCE_LIMIT

log = logging.getLogger(__name__)


def subscribe(request):
    if not request.user.is_authenticated():
        data = {'buttonname1': "register", 'buttonname2': "cancel", 'buttonname1_value': _("Register"),
                'buttonname2_value': _("Cancel"),
                'note': _("Register to system to participate in courses before the conferences")}
        form = CreateUserForm()
        if 'register' in request.POST:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save(commit=True)
                    user.set_password(user.password)
                    try:
                        user.save()
                        data['note'] = _("Your account has been created. Please check your email for activation link")
                    except Exception as e:
                        data['note'] = e.message
                    form = None
                except Exception as e:
                    data['note'] = _("Your account couldn't create. Please try again!")
                    log.error(e.message, extra=request.log_extra)
        elif 'cancel' in request.POST:
            return redirect("subscribe")
        data['createuserform'] = form
        return render(request, "userprofile/subscription.html", data)
    else:
        return redirect("selectcoursefcp")


@login_required(login_url='/')
def getaccomodations(request, usertype, gender):
    log.info("getaccomodation funtion call", extra=request.log_extra)
    jsondata = {}
    accomodations = Accommodation.objects.filter(
            usertype__in=[usertype, 'hepsi']).filter(
            gender__in=[gender, 'H']).filter(
            site=request.site).values_list('id', 'name').order_by('name')
    for a in accomodations:
        jsondata[a[0]] = a[1]
    return HttpResponse(json.dumps(jsondata), content_type="application/json")


@login_required(login_url='/')
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def createprofile(request):
    data = {}
    log.info("create/update profile form", extra=request.log_extra)
    data['update_user_form'] = UpdateUserForm(instance=request.user)
    data['note'] = "Profilinizi güncelleyebilirsiniz."
    note, userprobysite, data['userproform'], data['userproformbysite'], data['accomodations'], data[
        'accomodation_records'] = getuserprofileforms(request.user, request.site, request.log_extra)
    data['sitewidequestions'] = TextBoxQuestions.objects.filter(site=request.site, active=True, is_sitewide=True)
    if 'register' in request.POST:
        data['update_user_form'] = UpdateUserForm(data=request.POST, instance=request.user)
        try:
            data['userproform'] = StuProfileForm(request.POST, request.FILES, instance=request.user.userprofile,
                                                 ruser=request.user)
        except UserProfile.DoesNotExist:
            data['userproform'] = StuProfileForm(request.POST, request.FILES, ruser=request.user)
        if userprobysite:
            data['userproformbysite'] = UserProfileBySiteForm(request.POST, request.FILES, instance=userprobysite,
                                                              ruser=request.user, site=request.site)
        else:
            data['userproformbysite'] = UserProfileBySiteForm(request.POST, request.FILES, ruser=request.user,
                                                              site=request.site)
        if data['update_user_form'].is_valid():
            data['update_user_form'].save()
            if data['userproform'].is_valid():
                log.info("formvalid", extra=request.log_extra)
                try:
                    data['userproform'].save()
                    if data['sitewidequestions']:
                        for question in data['sitewidequestions']:
                            # noinspection PyUnresolvedReferences
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
                                log.info("Kullanıcı profilini ve konaklama tercihini güncelledi.",
                                         extra=request.log_extra)
                                if request.site.needs_document:
                                    if data['userproformbysite'].is_valid():
                                        data['userproformbysite'].save()
                                        if 'document' in request.FILES:
                                            log.info("Kullanıcı evrakını güncelledi.", extra=request.log_extra)
                                    else:
                                        data['note'] = "Profiliniz aşağıdaki sebeplerden dolayı kaydedilemedi"
                                        return render(request, "userprofile/user_profile.html", data)
                            except Exception as e:
                                log.error(e.message, extra=request.log_extra)
                                data['note'] = "Profiliniz kaydedildi ancak konaklama tercihleriniz kaydedilemedi." \
                                               " Sistem yöneticisi ile görüşün!"
                                return render(request, "userprofile/user_profile.html", data)
                    data['note'] = "Profiliniz başarılı bir şekilde kaydedildi. Kurs tercihleri adımından" \
                                   " devam edebilirsiniz"
                    return render(request, "userprofile/user_profile.html", data)
                except Exception as e:
                    log.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), extra=request.log_extra)
                    log.error(e.message, extra=request.log_extra)
                    data['note'] = "Profiliniz kaydedilirken hata oluştu lütfen sayfayı yeniden yükleyip tekrar deneyin"
                    return render(request, "userprofile/user_profile.html", data)
        data['note'] = "Profiliniz aşağıdaki sebeplerden dolayı oluşturulamadı"
    elif 'cancel' in request.POST:
        return redirect("createprofile")
    return render(request, "userprofile/user_profile.html", data)


@login_required(login_url='/')
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def instructor_information_view(request):
    if not request.user.userprofile:
        log.error("Kullanıcı Profili Bulunamadı", extra=request.log_extra)
        return redirect("createprofile")
    data = {}
    if not UserProfileOPS.is_instructor(request.user.userprofile):
        data['note'] = _("You are not authorized to access here")
    else:
        data['note'] = _("Please enter your transformation, arrival date, departure date information")
        try:
            instructorinformation = InstructorInformation.objects.get(user=request.user.userprofile, site=request.site)
            form = InstructorInformationForm(instance=instructorinformation, site=request.site, request=request)

        except ObjectDoesNotExist as e:
            log.debug("Egitmen bilgileri bulunamadi, yeni bilgiler olusturulmak icin form acilacak",
                      extra=request.log_extra)
            log.error(e.message, extra=request.log_extra)
            form = InstructorInformationForm(site=request.site, request=request)
            instructorinformation = None

        if request.POST:
            if instructorinformation is not None:
                form = InstructorInformationForm(request.POST, instance=instructorinformation, site=request.site,
                                                 request=request)
            else:
                form = InstructorInformationForm(request.POST, site=request.site, request=request)
            if form.is_valid():
                try:
                    instructor_info = form.save(commit=True)
                    data['note'] = _("Your information saved successfully")
                    log.info("%s egitmeni ek bilgilerini guncelledi" % instructor_info.user.user.username,
                             extra=request.log_extra)
                except Exception as e:
                    data['note'] = _("An error occurred while saving your information")
                    log.error(e.message, extra=request.log_extra)
        data['form'] = form
    return render(request, "userprofile/instructor_information.html", data)


@staff_member_required
def alluserview(request):
    """
    Kabul edilen tüm kullanıcıların konaklama bilgileri
    :param request:
    :return:
    """
    data = {}
    userlist = []
    try:
        allcourserecord = TrainessCourseRecord.objects.filter(course__site=request.site).values_list(
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
                    "accomodation": up.useraccomodationpref_set.filter(accomodation__site=request.site),
                    "courserecordid": "0"}
                try:
                    usr['document'] = up.userprofilebysite.document
                    usr['needs_document'] = up.userprofilebysite.needs_document
                except:
                    usr['document'] = None
                    usr['needs_document'] = False
                userlist.append(usr)
    except Exception as e:
        log.error("An error occured while showing alluserview", extra=request.log_extra)
        log.error(e.message, extra=request.log_extra)
    log.info("All user view showed", extra=request.log_extra)
    data["datalist"] = userlist
    return render(request, "userprofile/allusers.html", data)


@staff_member_required
def get_all_trainers_view(request):
    data = {}
    try:
        trainers = []
        courses = Course.objects.filter(site=request.site)
        for course in courses:
            trainers.extend(course.trainer.all())
        data['trainers'] = set(trainers)
    except Exception as e:
        log.error(e.message, extra=request.log_extra)
    return render(request, "userprofile/alltrainers.html", data)


def active(request, key):
    try:
        user_verification = UserVerification.objects.get(activation_key=key)
        if default_token_generator.check_token(user_verification.user, key):
            user = user_verification.user
            user.is_active = True
            user.save()
            backend_login(request, user)
    except ObjectDoesNotExist as e:
        log.error(e.message, extra=request.log_extra)
    except Exception as e:
        log.error(e.message, extra=request.log_extra)
    return redirect("createprofile")


def active_resend(request):
    data = {"note": _(
            "Please activate your account.  If you want to re-send an activation email, please click following button")}
    if request.POST:
        domain = request.site.home_url
        data['domain'] = domain.rstrip('/')
        user_verification, created = UserVerification.objects.get_or_create(user=request.user)
        user_verification.activation_key = create_verification_link(request.user)
        user_verification.save()
        data['activation_key'] = user_verification.activation_key
        data['recipientlist'] = [request.user.username]
        data["note"] = send_email_by_operation_name(data, "send_activation_key")
    return render(request, "userprofile/activate_resend.html", data)


@login_required(login_url='/')
def password_reset(request):
    data = {"note": _("Change your password")}
    form = ChangePasswordForm()
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                request.user.set_password(form.cleaned_data['password'])
                request.user.save()
                # noinspection PyTypeChecker
                backend_login(request, request.user)
                data['note'] = _("Your password has been changed")
                form = None
            except Exception as e:
                data['note'] = _("Your password couldn't be changed")
                log.error(e.message, extra=request.log_extra)
    data['changepasswordform'] = form
    return render(request, "userprofile/change_password.html", data)


def password_reset_key(request):
    data = {'note': _("Please enter your registered email")}
    if 'create' in request.POST:
        email = request.POST['email']
        if email and email != "":
            try:
                user = User.objects.get(email=request.POST['email'])
                user_verification, created = UserVerification.objects.get_or_create(user=user)
                user_verification.activation_key_expires = datetime.now() + timedelta(days=1)
                if request.POST.get('issms') == 'on':
                    password = User.objects.make_random_password()
                    user_verification.temporary_code = password
                    user_verification.save()
                    note = UserProfileOPS.send_sms(request, user, password)
                    if note.startswith("00"):
                        data['note'] = "SMS basarili bir sekilde gonderildi"
                        return redirect('password_reset_by_sms')
                    else:
                        data['note'] = "sms gonderilemedi: " + note

                else:
                    user_verification.password_reset_key = create_verification_link(user)
                    user_verification.save()
                    data['ruser'] = user
                    data['activation_key'] = user_verification.password_reset_key
                    domain = request.site.home_url
                    data['domain'] = domain.rstrip('/')
                    data['recipientlist'] = [user.username]
                    data['note'] = send_email_by_operation_name(data, "send_reset_password_key")
                if data['note']:
                    data['note'] = "Parola sıfırlama e-postası adresinize gönderildi."
                else:
                    data['note'] = "E-posta gönderilemedi"
            except ObjectDoesNotExist:
                data['note'] = _("""There isn't any user record with this e-mail on the system""")
                log.error(data['note'], extra=request.log_extra)
            #except Exception as e:
            #    data['note'] = _("""Password reset operation failed""")
            #    log.error(data['note'], extra=request.log_extra)
            #    log.error(e.message, extra=request.log_extra)
        else:
            data['note'] = _("""Email field can not be empty""")
            log.error(data['note'], extra=request.log_extra)
    return render(request, "userprofile/change_password_key_request.html", data)


def password_reset_key_done(request, note=None):
    data = {'note': _("Change your password")}
    form = ChangePasswordForm()
    try:
        user_verification = UserVerification.objects.get(password_reset_key=key)
        user = user_verification.user
        user.is_authenticated = False
        user.save()
        user_verification.delete()
        request.user = user
    except Exception as e:
        data['note'] = _("""Password reset operation failed""")
        log.error(e.message, extra=request.log_extra)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                request.user.set_password(form.cleaned_data['password'])
                request.user.save()
                data['note'] = _("""Your password has been changed""")
                form = None
                redirect("index")
            except Exception as e:
                data['note'] = _("""Your password couldn't be changed""")
                log.error(e.message, extra=request.log_extra)
    data['changepasswordform'] = form
    data['user'] = request.user
    return render(request, "userprofile/change_password.html", data)


def password_reset_by_sms(request):
    data = {'note': _("Change your password")}
    form = ChangePasswordWithSMSForm()
    if "updatepassword" in request.POST:
        form = ChangePasswordWithSMSForm(request.POST)
        if form.is_valid():
            try:
                user_verification = UserVerification.objects.get(temporary_code=form.cleaned_data.get('key'))
                if user_verification:
                    user = user_verification.user
                    user.is_authenticated = False
                    user.set_password(form.cleaned_data.get('password'))
                    user.save()
                    user_verification.delete()
                    return redirect('index')
                else:
                    data['note'] = "Geçersiz Kod"
            except Exception as e:
                data['note'] = _("""Password reset operation failed""")
                log.error(e.message, extra=request.log_extra)
    data['changepasswordform'] = form
    return render(request, "userprofile/change_password.html", data)


def backend_login(request, user):
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)


@login_required
def showuserprofile(request, userid, courserecordid):
    data = {}
    if UserProfileOPS.is_instructor(request.user.userprofile) or request.user.is_staff:
        courserecord = None
        try:
            courserecord = TrainessCourseRecord.objects.get(pk=courserecordid,
                                                            trainess=UserProfile.objects.get(pk=userid))
            if not UserProfileOPS.is_user_trainer_ofcourse_or_staff(request.user, courserecord.course):
                return redirect("selectcoursefcp")
        except Exception as e:
            log.warning(e.message, extra=request.log_extra)
            if not request.user.is_staff:
                return redirect("selectcoursefcp")
            log.warning("Staff user show user profile", extra=request.log_extra)
        user = UserProfile.objects.get(pk=userid)
        data['tuser'] = user
        data['ruser'] = request.user
        data['note'] = "Detaylı kullanıcı bilgileri"
        if user:
            userprofilebysite = None
            try:
                userprofilebysite = UserProfileBySite.objects.get(user=user.user, site=request.site)
                data['userprofilebysiteform'] = UserProfileBySiteForStaffForm(instance=userprofilebysite,
                                                                              ruser=request.user, site=request.site,
                                                                              user=user.user)
            except UserProfileBySite.DoesNotExist as e:
                data['userprofilebysiteform'] = UserProfileBySiteForStaffForm(ruser=request.user, site=request.site,
                                                                              user=user.user)
            if "savesitebasedprofile" in request.POST:
                if userprofilebysite:
                    data['userprofilebysiteform'] = UserProfileBySiteForStaffForm(request.POST, request.FILES,
                                                                                  instance=userprofilebysite,
                                                                                  ruser=request.user, site=request.site,
                                                                                  user=user.user)
                else:
                    data['userprofilebysiteform'] = UserProfileBySiteForStaffForm(request.POST, request.FILES,
                                                                                  ruser=request.user, site=request.site,
                                                                                  user=user.user)
                if data['userprofilebysiteform'].is_valid():
                    data['userprofilebysiteform'].save()
                    log.info("%s kullanıcısı için etkinlik bazlı profil kaydedildi", extra=request.log_extra)
                    data['note'] = "Etkinlik bazlı profil kaydedildi."
                else:
                    data['note'] = "Kullanici bazlı profil formu doğrulanamadı."
            if request.user.is_staff and "cancelall" in request.POST:
                cancelnote = request.POST.get('trainesscancelnotetext', '')
                res = cancel_all_prefs(user, cancelnote, request.site, request.user, request.log_extra)
                if res == 1:
                    data['note'] = "Kullanıcının Tüm Başvuruları Silindi"
                else:
                    data['note'] = "Kullanıcının Başvuruları silinirken hata oluştu"
            if "savescore" in request.POST:
                '''
                    Kullanıcı için not girişi
                '''
                trainessnote = request.POST.get('trainessnotetext')
                data['note'] = UserProfileOPS.savenote(request, user.user, trainessnote)
            if courserecord:
                '''
                    Kullanıcı profilindeki yoklamalar buradan alınıyor. (Görevli kullanıcı erişebilir)
                '''
                data['courseid'] = courserecord.course.pk
                if request.user.is_staff and courserecord.consentemailsent:
                    try:
                        data['forms'] = getparticipationforms(request.site, courserecord)
                        if "save" in request.POST:
                            data['note'] = UserProfileOPS.saveparticipation(request, courserecord)
                            data['forms'] = getparticipationforms(request.site, courserecord)
                    except Exception as e:
                        log.error(e.message, extra=request.log_extra)
        else:
            data['note'] = "Böyle Bir kullanıcı yoktur."
        return render(request, "userprofile/showuserprofile.html", data)
    return redirect("controlpanel")
