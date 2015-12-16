# -*- coding:utf-8  -*-
import logging
import hashlib
import random
from django.shortcuts import render, render_to_response, redirect
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as logout_user
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

<<<<<<< HEAD
from userprofile.forms import CreateUserForm, InstProfileForm, StuProfileForm, AccomodationPrefForm
from userprofile.models import SubscribeNotice,Accommodation,UserAccomodationPref,UserProfile
=======
from userprofile.forms import CreateUserForm, InstProfileForm, StuProfileForm
from userprofile.models import SubscribeNotice, UserVerification
>>>>>>> 673d3a1e2f938ce2bcda8a7cab6f080161aa7fcd

from abkayit.models import *
from abkayit.settings import USER_TYPES,GENDER
from abkayit.backend import prepare_template_data

log=logging.getLogger(__name__)

@csrf_exempt
def loginview(request):
	# TODO: kullanici ve parola hatali ise ve login olamazsa bir login sayfasina yonlendirilip capcha konulmasi csrf li form ile username password alinmasi gerekiyor
	state=""
	alerttype=""
	if not request.user.is_authenticated():
		username=""
		password=""
		alerttype="alert-info"
		state="Hesabiniz varsa buradan giris yapabilirsiniz!"
		if request.POST:
			username=request.POST['username']
			password=request.POST['password']
			user=authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
				log.info("%s user successfuly logged in" % (request.user),extra={'clientip': request.META['REMOTE_ADDR'], 'user': request.user})
	return HttpResponseRedirect('/')

def subscribe(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = prepare_template_data(request)    
    if not request.user.is_authenticated():
        data['buttonname1']="register"
        data['buttonname2']="cancel"
        note = _("Register to system to give training,  participation in courses before the conferences, and  participation in conferences.")
        form = CreateUserForm()
        if 'register' in request.POST:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save(commit=True)
                    user.set_password(user.password)
                    user.save()
                    note = _("""Your account created. You can give course proposal, you can register in courses before the conferences, 
                                and you can register to the conferences""")
                    form = None
                except Exception as e:
                    note="Hesap olusturulamadi. Lutfen daha sonra tekrar deneyin!"
                    log.error(e.message, extra=d)
        elif 'cancel' in request.POST:
            return redirect("index")
        data['createuserform']=form
        data['note']=note
        return render_to_response("userprofile/subscription.html",data,context_instance=RequestContext(request))
    else:
        return redirect("controlpanel")

def createprofile(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = prepare_template_data(request)
    data['buttonname1']='next'
    data['buttonname2']='cancel'
    form=StuProfileForm()
    note=_("Isleme devam edebilmek icin lutfen profilinizi tamamlayın")
    gender=''
    if 'next' in request.POST:
        form=StuProfileForm(request.user,request.POST)
        if form.is_valid():
            gender=form.cleaned_data['gender']
            try:
                profile=form.save(commit=False)
                profile.is_student=True
                profile.user=User.objects.get(email=request.user)
                profile.save()
                note=_("Profil kaydedildi. Lütfen konaklama seciminizi yapin")
            except:
                note=_("Kullanıcı profili oluşturulurken hata olustu. Lütfen sistem yöneticiniz ile iletişime geciniz")
            achoices=Accommodation.objects.filter(usertype__in=['stu','hepsi']).filter(gender__in=[gender,'H']).values_list('id','name').order_by('name')
            form = AccomodationPrefForm(achoices)
            data['buttonname1']='register'
    elif 'register' in request.POST:
        gender=UserProfile.objects.get(user=User.objects.get(email=request.user)).gender
        achoices=Accommodation.objects.filter(usertype__in=['stu','hepsi']).filter(gender__in=[gender,'H']).values_list('id','name').order_by('name')
        form = AccomodationPrefForm(achoices,request.POST)
        if form.is_valid():
            if form.cleaned_data['accomodation']:
                try:
                    counter=0
                    for a in form.cleaned_data['accomodation']:
                        counter+=1
                        uaccpref=UserAccomodationPref(user=UserProfile.objects.get(user=request.user.pk),accomodation=Accommodation.objects.get(pk=a),usertype="stu",preference_order=counter)
                        uaccpref.save()
                    return redirect("applytocourse")
                except:
                    note=_("Profil oluşturuldu ancak konaklama tercihi olusturulurken hata olustu.")
            else:
                note=_("Lütfen aşağıdaki alanları doldurun!")
        else:
            note=_("Lutfen asagidaki alanları doldurun")
    elif 'cancel' in request.POST:
        return redirect("index")
    data['createuserform']=form
    data['note']=note
    return render_to_response("userprofile/subscription.html",data,context_instance=RequestContext(request))

def activate(request, key):
    user_verification = UserVerification.objects.get(activation_key=key)
    if user_verification:
        user = User.objects.get(username=user_verification.user_email)
        user.is_active=True
        user.save()
        return HttpResponse("kullanici aktif edildi")

def logout(request):
	logout_user(request)
	return HttpResponseRedirect("/")


