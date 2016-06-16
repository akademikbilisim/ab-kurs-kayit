# -*- coding:utf-8  -*-
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
from django.conf import settings

from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required

from userprofile.forms import CreateUserForm, UpdateUserForm, StuProfileForm, InstructorInformationForm, \
    ChangePasswordForm
from userprofile.models import Accommodation, UserProfile, UserAccomodationPref, InstructorInformation, \
    UserVerification, TrainessNote
from training.tutils import getparticipationforms
from training.forms import ParticipationForm
from training.models import Course, TrainessCourseRecord

from abkayit.models import *
from abkayit.backend import getsiteandmenus, create_verification_link, send_email_by_operation_name

from abkayit.decorators import active_required

from abkayit.settings import ACCOMODATION_PREFERENCE_LIMIT

log = logging.getLogger(__name__)


def subscribe(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    if not request.user.is_authenticated():
        data['buttonname1'] = "register"
        data['buttonname2'] = "cancel"
        data['buttonname1_value'] = _("Register")
        data['buttonname2_value'] = _("Cancel")
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
        return redirect("controlpanel")


@login_required(login_url='/')
def getaccomodations(request, usertype, gender):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
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
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    log.info("create profile form", extra=d)
    data['update_user_form'] = UpdateUserForm(instance=request.user)
    data['accomodations_preference_count'] = range(ACCOMODATION_PREFERENCE_LIMIT)
    data['form'] = None
    try:
        user_profile = request.user.userprofile
        note = _("You can update your profile below")
        data['form'] = StuProfileForm(instance=user_profile)
        if not user_profile.is_instructor:
            log.debug("egitmen olmayan kullanici icin isleme devam ediliyor", extra=d)
            data['accomodations'] = Accommodation.objects.filter(
                usertype__in=['stu', 'hepsi'], gender__in=[user_profile.gender, 'H'], site=data['site']).order_by(
                'name')
            data['accomodation_records'] = UserAccomodationPref.objects.filter(user=user_profile).order_by(
                'preference_order')
    except UserProfile.DoesNotExist:
        note = _("If you want to continue please complete your profile.")
        data['form'] = StuProfileForm()
        data['accomodations'] = Accommodation.objects.filter(usertype__in=['stu', 'hepsi'], gender__in=['K', 'E', 'H'],
                                                             site=data['site']).order_by('name')
    if 'register' in request.POST:
        data['update_user_form'] = UpdateUserForm(data=request.POST, instance=request.user)
        try:
            data['form'] = StuProfileForm(data=request.POST, instance=request.user.userprofile, ruser=request.user)
        except UserProfile.DoesNotExist:
            data['form'] = StuProfileForm(request.POST, ruser=request.user)
        if data['update_user_form'].is_valid() and data['form'].is_valid():
            log.info("formvalid", extra=d)
            try:
                profile = data['form'].save(commit=False)
                profile.user = request.user
                profile.save()
                if not request.user.userprofile.is_instructor and ACCOMODATION_PREFERENCE_LIMIT:
                    prefs = UserAccomodationPref.objects.filter(user=request.user.userprofile)
                    if prefs:
                        prefs.delete()
                    for pref in range(0, len(data['accomodations'])):
                        if 'tercih' + str(pref + 1) in request.POST.keys():
                            try:
                                uaccpref = UserAccomodationPref(user=profile,
                                                                accomodation=Accommodation.objects.get(
                                                                    pk=request.POST['tercih' + str(pref + 1)]),
                                                                usertype="stu", preference_order=pref + 1)
                                uaccpref.save()
                                note = "Profiliniz başarılı bir şekilde kaydedildi. Kurs tercihleri adımından" \
                                       " devam edebilirsiniz"
                            except Exception as e:
                                log.error(e.message, extra=d)
                                note = "Profiliniz kaydedildi ancak konaklama tercihleriniz kaydedilemedi." \
                                       " Sistem yöneticisi ile görüşün!"
                else:
                    note = "Profiliniz başarılı bir şekilde kaydedildi. Kurs tercihleri adımından" \
                       " devam edebilirsiniz"
            except Exception as e:
                log.error(e.message, extra=d)
                note = "Profiliniz kaydedilirken hata oluştu lütfen sayfayı yeniden yükleyip tekrar deneyin"
        else:
            note = "Profiliniz aşağıdaki sebeplerden dolayı oluşturulamadı"
    elif 'cancel' in request.POST:
        return redirect("createprofile")
    data['note'] = note
    return render_to_response("userprofile/user_profile.html", data, context_instance=RequestContext(request))


@login_required(login_url='/')
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def instructor_information(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    if not request.user.userprofile:
        log.error("Kullanıcı Profili Bulunamadı", extra=d)
        return redirect("createprofile")
    data = getsiteandmenus(request)
    if not request.user.userprofile.is_instructor:
        note = _("You don't have permission to access to here")
    else:
        note = _("Please enter your transformation, arrival date, departure date informations")
        instructorinformation = None
        try:
            instructorinformation = InstructorInformation.objects.get(user=request.user.userprofile)
            form = InstructorInformationForm(instance=instructor_information)
        except Exception as e:
            log.debug("Egitmen bilgileri bulunamadi, yeni bilgiler olusturulmak icin form acilacak", extra=d)
            log.error(e.message, extra=d)
            form = InstructorInformationForm()
        if request.POST:
            if instructorinformation:
                form = InstructorInformationForm(request.POST, instance=instructorinformation)
            else:
                form = InstructorInformationForm(request.POST)
            if form.is_valid():
                try:
                    form.instance.user = request.user.userprofile
                    instructor_info = form.save(commit=True)
                    instructor_info.user = request.user.userprofile
                    instructor_info.save()
                    note = _("Your informations saved successfully")
                except Exception as e:
                    note = _("Error occured during save your informations")
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
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    userlist = []
    allcourserecord = TrainessCourseRecord.objects.filter(course__site=data['site'], approved=True)
    if allcourserecord:
        for r in allcourserecord:
            usr = {"usertype": "student", "firstname": r.trainess.user.first_name,
                   "email": r.trainess.user.username, "lastname": r.trainess.user.last_name,
                   "tcino": r.trainess.tckimlikno if r.trainess.tckimlikno != '' else r.trainess.ykimlikno,
                   "coursename": r.course.name,
                   "gender": r.trainess.gender,
                   "accomodation": UserAccomodationPref.objects.filter(user=r.trainess)}
            userlist.append(usr)
    data["datalist"] = userlist
    return render_to_response("userprofile/allusers.html", data, context_instance=RequestContext(request))


@staff_member_required
def get_all_trainers_view(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    try:
        trainers = UserProfile.objects.filter(is_instructor=True)
        data['trainers'] = trainers
    except Exception as e:
        log.error(e.message, extra=d)
    return render_to_response("userprofile/alltrainess.html", data, context_instance=RequestContext(request))


def active(request, key):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    try:
        user_verification = UserVerification.objects.get(activation_key=key)
        user = User.objects.get(username=user_verification.user_email)
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
        user_verification, created = UserVerification.objects.get_or_create(user_email=request.user.username)
        user_verification.activation_key = create_verification_link(request.user)
        user_verification.save()
        data['activation_key'] = user_verification.activation_key
        data['recipientlist'] = [request.user.username]
        note = send_email_by_operation_name(data, "send_confirm")
    data['note'] = note
    return render_to_response("userprofile/activate_resend.html", data, context_instance=RequestContext(request))


@login_required(login_url='/')
def password_reset(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
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
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    note = _("Please enter your registered email")
    if request.method == 'POST':
        email = request.POST['email']
        if email and email != "":
            try:
                user = User.objects.get(username=request.POST['email'])
                user_verification, created = UserVerification.objects.get_or_create(user_email=user.username)
                user_verification.password_reset_key = create_verification_link(user)
                user_verification.save()
                data['user'] = user
                data['activation_key'] = user_verification.password_reset_key
                domain = data['site'].home_url
                data['domain'] = domain.rstrip('/')
                note = send_email_by_operation_name(data, "send_reset_password_key")
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
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    form = ChangePasswordForm()
    note = _("Change your password")
    try:
        user_verification = UserVerification.objects.get(password_reset_key=key)
        user = User.objects.get(username=user_verification.user_email)
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
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    jsondata = {}
    if request.method == 'POST':
        trainess_username = request.POST['trainess_username']
        t_note = request.POST['note']
        if trainess_username and trainess_username != '':
            try:
                userprofile = UserProfile.objects.get(user__username=trainess_username)
                trainess_note = TrainessNote.objects.create(note_to_profile=userprofile, site=data['site'])
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


@staff_member_required
def showuserprofile(request, userid, courserecordid):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    user = UserProfile.objects.get(pk=userid)
    courserecord = TrainessCourseRecord.objects.get(pk=courserecordid)
    if user:
        data['note'] = "Detaylı kullanıcı bilgileri"
        data['tuser'] = user
        data['forms'] = getparticipationforms(data['site'], courserecord)
        if request.POST:
            formsarevalid = []
            frms = []
            for f in data['forms']:
                frm = ParticipationForm(request.POST,
                                        prefix="participation" + str(
                                            datetime.strptime(f.initial['day'], '%Y-%m-%d').day))
                frm.courserecord = courserecord.pk
                frm.day = f.initial['day']
                formsarevalid.append(frm.is_valid())
                frms.append(frm)
            print formsarevalid
            if all(formsarevalid):
                for f in frms:
                    f.save()
                data['note'] = 'Seçimleriniz başarıyla kaydedildi.'
                log.info("%s nolu kurs kaydinin yoklama kaydi girişi başarılı" % courserecord.pk, extra=d)
            else:
                data['note'] = 'Hata oluştu!'
                log.info("%s nolu kurs kaydinin yoklama kaydi girişi hatalı" % courserecord.pk, extra=d)
    else:
        data['note'] = "Böyle Bir kullanıcı yoktur."

    return render_to_response("userprofile/showuserprofile.html", data, context_instance=RequestContext(request))
