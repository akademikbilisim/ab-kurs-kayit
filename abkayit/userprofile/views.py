# -*- coding:utf-8  -*-
import json
import logging

from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import user_passes_test, login_required
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from userprofile.forms import *
from userprofile.models import *

from abkayit.models import *
from abkayit.backend import create_verification_link
from abkayit.adaptor import send_email
from abkayit.decorators import active_required

from training.models import Course
from userprofile.userprofileops import UserProfileOPS

logger = logging.getLogger(__name__)


def subscribe(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = dict()
    if not request.user.is_authenticated():
        state = "Katılımcı olmak için sisteme kaydolunuz!"
        alert_type = "alert-info"
        create_user_form = CreateUserForm()
        if request.POST:
            create_user_form = CreateUserForm(request.POST)
            if create_user_form.is_valid():
                try:
                    user = create_user_form.save(commit=True)
                    user.set_password(user.password)
                    user.save()
                    state = "Hesabınız oluşturuldu, doğrulama linki için e-postanızı kontrol ediniz!"
                    alert_type = "alert-success"
                    create_user_form = None
                except Exception as e:
                    state = "Hesabınız oluşturulurken hata oluştu, lütfen tekrar deneyiniz!"
                    alert_type = "alert-danger"
                    logger.error(e.message, extra=d)
        data['create_user_form'] = create_user_form
        data['state'] = state
        data['alert_type'] = alert_type
        return render(request, "subscription.html", data)
    else:
        return redirect("control_panel")


@login_required(login_url='/')
def accommodations(request, user_type, gender):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    json_data = {}
    try:
        accomodations = Accommodation.objects.filter(
            usertype__in=[user_type, 'hepsi']).filter(
            gender__in=[gender, 'H']).filter(
            site=Site.objects.get(is_active=True)).values_list('id', 'name').order_by('name')
    except Exception as e:
        logger.error(e.message, extra=d)
    for a in accomodations:
        json_data[a[0]] = a[1]
    return HttpResponse(json.dumps(json_data), content_type="application/json")


@login_required
def profile(request):
    data = {}
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    if request.POST:
        try:
            userprofile_form = UserProfileForm(request.POST, prefix='userprofile_form',
                                               instance=request.user.userprofile)
        except ObjectDoesNotExist:
            userprofile_form = UserProfileForm(request.POST, prefix='userprofile_form')
        user_form = UpdateUserForm(request.POST, prefix='user_form', instance=request.user)
        if all([userprofile_form.is_valid(), user_form.is_valid()]):
            user_profile_ops = UserProfileOPS()
            tck_is_valid = user_profile_ops.validate_tckimlik_no(
                userprofile_form.cleaned_data['tckimlikno'].rstrip().lstrip(),
                user_form.cleaned_data['first_name'].rstrip().lstrip(),
                user_form.cleaned_data['last_name'].rstrip().lstrip(),
                userprofile_form.cleaned_data['birthdate'].year)
            if tck_is_valid == -1:
                state = "Tc kimlik numarası doğrulaması sırasında hata oluştu"
                alert_type = "alert-danger"
            elif not tck_is_valid:
                state = "Tc kimlik numarası doğrulamadı, lütfen Tc kimlik numaranızı, isminizi, " \
                        "soyisminizi(Türkçe karakterlerle birlikte) ve doğum tarihinizi eksiksiz doldurunuz"
                alert_type = "alert-danger"
            else:
                user = user_form.save()
                profile = userprofile_form.save(commit=False)
                profile.user = user
                profile.save()
                state = "Bilgileriniz kaydedildi"
                alert_type = "alert-success"
        else:
            state = "Bilgileriniz kaydedilemedi"
            alert_type = "alert-danger"
            logger.error("forms are not valid")
    else:
        user_form = UpdateUserForm(instance=request.user, prefix='user_form')
        try:
            userprofile_form = UserProfileForm(prefix='userprofile_form', instance=request.user.userprofile)
        except ObjectDoesNotExist:
            userprofile_form = UserProfileForm(prefix='userprofile_form')
        state = "Bilgilerinizi güncelleyebilirsiniz"
        alert_type = "alert-info"
    data['state'] = state
    data['alert_type'] = alert_type
    data['userprofile_form'] = userprofile_form
    data['user_form'] = user_form
    return render(request, "user_profile.html", data)


@login_required(login_url='/')
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def trainer_information(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = dict()
    if request.user.userprofile is None:
        logger.error("Kullanıcı Profili Bulunamadı", extra=d)
        return redirect("profile")
    state = "Lütfen ulaşım, geliş ve gidiş tarih bilgilerinizi giriniz!"
    alert_type = "alert-info"
    if not request.user.userprofile.is_instructor:
        state = "Buraya erişim izniniz yok!"
        alert_type = "alert-danger"
    else:
        instructor_information = None
        try:
            instructor_information = InstructorInformation.objects.get(user=request.user.userprofile)
        except ObjectDoesNotExist as e:
            logger.error(e.message, extra=d)
        if request.POST:
            form = InstructorInformationForm(request.POST, instance=instructor_information)
            if form.is_valid():
                try:
                    form.instance.user = request.user.userprofile
                    instructor_info = form.save(commit=True)
                    instructor_info.user = request.user.userprofile
                    instructor_info.save()
                    state = "Bilgileriniz kaydedildi!"
                    alert_type = "alert-success"
                except Exception as e:
                    state = "Bilgileriniz kaydedilirken hata oluştu!"
                    alert_type = "alert-danger"
                    logger.error(e.message, extra=d)
        else:
            if instructor_information:
                form = InstructorInformationForm(instance=instructor_information)
            else:
                form = InstructorInformationForm()

        data['form'] = form
    data['state'] = state
    data['alert_type'] = alert_type
    return render(request, "instructor_information.html", data)


@staff_member_required
def all_users(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = dict()
    user_list = []
    alluser = UserProfile.objects.all()
    if alluser:
        for u in alluser:
            usr = dict()
            usr["usertype"] = "instructor" if u.is_instructor else "student"
            usr["firstname"] = u.user.first_name
            usr["lastname"] = u.user.last_name
            usr["tcino"] = u.tckimlikno if u.tckimlikno != '' else u.ykimlikno
            usr["coursename"] = Course.objects.filter(trainer=u).values_list('name', flat=True)
            usr["accomodation"] = UserAccomodationPref.objects.filter(user=u)
            user_list.append(usr)
    data["datalist"] = user_list
    return render(request, "allusers.html", data)


@staff_member_required
def all_trainers(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = dict()
    try:
        trainers = UserProfile.objects.filter(is_instructor=True)
        data['trainers'] = trainers
    except Exception as e:
        logger.error(e.message)
    return render(request, "alltrainess.html", data)


def active(request, key):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    try:
        user_verification = UserVerification.objects.get(activation_key=key)
        user = User.objects.get(username=user_verification.user_email)
        user.is_active = True
        user.save()
        backend_login(request, user)
        user_verification.delete()
    except ObjectDoesNotExist as e:
        logger.error(e.message, extra=d)
    except Exception as e:
        logger.error(e.message, extra=d)
    return redirect("profile")


def active_resend(request):
    data = dict()
    state = "Lütfen hesabınızı aktifleştirin, eğer aktifleştirme linkini tekrar almak istiyorsanız " \
            "lütfen aşağıdaki düğmeye tıklayınız!"
    alert_type = "alert-info"
    if request.POST:
        user = request.user
        context = dict()
        context['user'] = user

        domain = Site.objects.get(is_active=True).home_url
        if domain.endswith('/'):
            domain = domain.rstrip('/')
        context['domain'] = domain

        user_verification, created = UserVerification.objects.get_or_create(user_email=user.username)
        user_verification.activation_key = create_verification_link(user)
        user_verification.save()
        context['activation_key'] = user_verification.activation_key
        try:
            send_email("messages/send_confirm_subject.html",
                       "messages/send_confirm.html",
                       "messages/send_confirm.text",
                       context,
                       settings.EMAIL_FROM_ADDRESS,
                       [user.username])

            state = "Aktifleştirme linki e-posta adresinize gönderildi!"
            alert_type = "alert-success"
        except Exception as e:
            state = e.message
    data['state'] = state
    data['alert_type'] = alert_type
    return render(request, "activate_resend.html", data)


@login_required(login_url='/')
def password_reset(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = dict()
    state = "Parolanızı değiştirebilirsiniz"
    alert_type = "alert-info"
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                request.user.set_password(form.cleaned_data['password'])
                request.user.save()
                backend_login(request, request.user)
                state = "Parolanız değiştirildi"
                messages.add_message(request, messages.SUCCESS, state)
                request.user.message_
            except Exception as e:
                logger.error("Parola değiştirme sırasında hata olustu", e.message, extra=d)
                state = "Parolanız değiştirilirken hata oluştu!"
                alert_type = "alert-danger"
        else:
            logger.error("Parola degistirme formu dogrulanamadi")
            state = "Parolanız değiştirilirken hata oluştu!"
            alert_type = "alert-danger"
    else:
        form = ChangePasswordForm()
    data['change_password_form'] = form
    data['state'] = state
    data['alert_type'] = alert_type
    return render(request, "change_password.html", data)


def password_reset_key(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = dict()
    state = "Lütfen kayıtlı e-posta adresinizi giriniz"
    alert_type = "alert-info"
    if request.method == 'POST':
        email = request.POST['email']
        if email:
            try:
                user = User.objects.get(username=request.POST['email'])
                user_verification, created = UserVerification.objects.get_or_create(user_email=user.username)
                user_verification.password_reset_key = create_verification_link(user)
                user_verification.save()
                context = dict()
                context['user'] = user
                context['activation_key'] = user_verification.password_reset_key
                domain = Site.objects.get(is_active=True).home_url
                if domain.endswith('/'):
                    domain = domain.rstrip('/')
                context['domain'] = domain
                send_email("messages/send_reset_password_key_subject.html",
                           "messages/send_reset_password_key.html",
                           "messages/send_reset_password_key.text",
                           context,
                           settings.EMAIL_FROM_ADDRESS,
                           [user.username])
                state = "Parola sıfırlama linki e-posta adresinize gönderildi!"
                alert_type = "alert-success"
            except ObjectDoesNotExist as e:
                state = "Sistemde bu e-posta adresiyle herhangi bir kullanıcı bulunamadı"
                alert_type = "alert-danger"
                logger.error(e.message, extra=d)
            except Exception as e:
                state = "Parola sıfırlama işleminde hata oluştu!"
                alert_type = "alert-danger"
                logger.error(e.message, extra=d)
        else:
            state = "E-posta alanı boş olamaz!"
            alert_type = "alert-danger"
            logger.error(state, extra=d)
    data['state'] = state
    data['alert_type'] = alert_type
    return render(request, "change_password_key_request.html", data)


def password_reset_key_done(request, key=None):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = dict()
    state = "Parolanızı değiştirin"
    alert_type = "alert-info"
    form = ChangePasswordForm()
    try:
        user_verification = UserVerification.objects.get(password_reset_key=key)
        user = User.objects.get(username=user_verification.user_email)
        user.is_authenticated = False
        user.save()
        request.user = user
    except Exception as e:
        state = "Parola sıfırlama işleminde hata oluştu!"
        alert_type = "alert-danger"
        logger.error(e.message, extra=d)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                request.user.set_password(form.cleaned_data['password'])
                request.user.save()
                state = "Paronız değiştirildi"
                alert_type = "alert-success"
                data['state'] = state
                data['alert_type'] = alert_type
                return redirect("index")
            except Exception as e:
                state = "Parolanız değiştirilemedi!"
                alert_type = "alert-danger"
                logger.error(e.message, extra=d)
    data['change_password_form'] = form
    data['state'] = state
    data['alert_type'] = alert_type
    data['user'] = request.user
    return render(request, "change_password.html", data)


@login_required(login_url='/')
def save_note(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = dict()
    jsondata = {}
    if request.method == 'POST':
        trainess_username = request.POST['trainess_username']
        trainess_score = request.POST['score']
        t_note = request.POST['note']
        if trainess_username and trainess_username != '':
            try:
                userprofile = UserProfile.objects.get(user__username=trainess_username)
                userprofile.score = trainess_score
                userprofile.save()
                trainess_note, created = TrainessNote.objects.get_or_create(note_to_profile=userprofile,
                                                                            site=data['site'])
                trainess_note.note = t_note
                trainess_note.note_from_profile = request.user.userprofile
                trainess_note.note_date = datetime.now()
                trainess_note.save()
                jsondata['status'] = "0"
                jsondata['message'] = "Durum güncellendi!"
            except Exception as e:
                jsondata['status'] = "-1"
                jsondata['message'] = "Durum güncelleme sırasında hata olustu"
                logger.error(e.message, extra=d)
        else:
            jsondata['status'] = "-1"
            jsondata['message'] = "Hata: Kullanıcı adı boş olamaz!"
            logger.error("username bos olamaz", extra=d)

    return HttpResponse(json.dumps(jsondata), content_type="application/json")


def logout(request):
    logout_user(request)
    return HttpResponseRedirect("/")


def backend_login(request, user):
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
