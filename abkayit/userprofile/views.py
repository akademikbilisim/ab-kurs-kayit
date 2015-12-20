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
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import *
from django.core.urlresolvers import reverse_lazy

from userprofile.forms import *
from userprofile.models import *

from abkayit.models import *
from abkayit.backend import prepare_template_data, create_verification_link
from abkayit.adaptor import send_email
from abkayit.settings import USER_TYPES,GENDER
from abkayit.decorators import active_required

log = logging.getLogger(__name__)

@csrf_exempt
def loginview(request):
	# TODO: kullanici ve parola hatali ise ve login olamazsa bir login sayfasina yonlendirilip capcha konulmasi csrf li form ile username password alinmasi gerekiyor
	d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
	state = ""
	alerttype = ""
	if not request.user.is_authenticated():
		username = ""
		password = ""
		alerttype = "alert-info"
		state = _("If you have account, you can enter from here!")
		if request.POST:
			username=request.POST['username']
			password=request.POST['password']
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
				log.info("%s user successfuly logged in" % (request.user), extra=d)
	return HttpResponseRedirect('/')

def subscribe(request):
	d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
	data = prepare_template_data(request)	
	if not request.user.is_authenticated():
		data['buttonname1'] = "register"
		data['buttonname2'] = "cancel"
		note = _("Register to system to participate in courses before the conferences")
		form = CreateUserForm()
		if 'register' in request.POST:
			form = CreateUserForm(request.POST)
			if form.is_valid():
				try:
					user = form.save(commit=True)
					user.set_password(user.password)
					user.save()
					note = _("Your account has been created. Please check your email for activation link")
					form = None
				except Exception as e:
					note = _("Your account couldn't create. Please try again!")
					log.error(e.message, extra=d)
		elif 'cancel' in request.POST:
			return redirect("index")
		data['createuserform'] = form
		data['note']=note
		return render_to_response("userprofile/subscription.html", data, context_instance=RequestContext(request))
	else:
		return redirect("controlpanel")

@login_required(login_url='/')
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def createprofile(request):
	d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
	data = prepare_template_data(request)

	note = _("If you want to continue please complete your profile. Accomodation options will be enable to select after create profile")

	update_user_form = UpdateUserForm()
	form = StuProfileForm()
	accomodation_form = None
	try:
		user = User.objects.get(username=request.user.username)	
		update_user_form = UpdateUserForm(instance=user)
		form = StuProfileForm(instance=UserProfile.objects.get(user=user))
		try:
			user_profile = UserProfile.objects.get(user=user)
			form = StuProfileForm(instance=user_profile)
			achoices=Accommodation.objects.filter(
				usertype__in=['stu','hepsi']).filter(
				gender__in=[user_profile.gender,'H']).values_list('id','name').order_by('name')
			accomodation_form = AccomodationPrefForm(achoices=achoices)
			note = _("You can update your profile")
		except Exception as e:
			log.error(e.message, extra=d)
	except Exception as e:
		log.error(e.message, extra=d)

	if 'register' in request.POST:
		first_name = request.POST.get('first_name','')
		last_name = request.POST.get('last_name','')
		form = StuProfileForm(request.user, request.POST, ruser=request.user)
		try:
			form.instance = UserProfile.objects.get(user=request.user)
		except Exception as e:
			log.info("Createing new profile", extra=d)
		if form.is_valid():
			if first_name or last_name:
				user = User.objects.get(username=request.user.username)
				user.first_name=first_name
				user.last_name=last_name
				user.save()
			profile = form.save(commit=False)
			profile.is_student = True
			profile.user = User.objects.get(email=request.user)
			profile.save()
			achoices=Accommodation.objects.filter(
				usertype__in=['stu','hepsi']).filter(
				gender__in=[user_profile.gender,'H']).values_list('id','name').order_by('name')
			accomodation_form = AccomodationPrefForm(achoices=achoices)
			note = _("Your profile has been updated")	   	
	if 'cancel' in request.POST:
		return redirect("createprofile")	
	data['update_user_form'] = update_user_form
	data['form'] = form
	data['accomodation_form'] = accomodation_form
	data['note'] = note
	return render_to_response("userprofile/user_profile.html",data,context_instance=RequestContext(request))


def active(request, key):
	d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
	try:
		user_verification = UserVerification.objects.get(activation_key=key)
		user = User.objects.get(username=user_verification.user_email)
		user.is_active=True
		user.is_authenticated=True
		user.save()
	except ObjectDoesNotExist as e:
		log.error(e.message, extra=d)
	except Exception as e:
		log.error(e.message, extra=d)
	return redirect("index")


def active_resend(request):
	data = prepare_template_data(request)
	note = _("Please activate your account.  If you want to re-send an activation email, please click following button") 
	if request.POST:
		user = request.user
		user_verification, created = UserVerification.objects.get_or_create(user_email=user.username)
		context={}
		context['user'] = user
		domain = Site.objects.get(is_active=True).home_url
		if domain.endswith('/'):
		    domain = domain.rstrip('/')
		context['domain'] = domain
		
		user_verification, created = UserVerification.objects.get_or_create(user_email=user.username)
		user_verification.activation_key = create_verification_link(user)
		user_verification.save()
		context['activation_key'] = user_verification.activation_key
		send_email("userprofile/messages/send_confirm_subject.html",
		                "userprofile/messages/send_confirm.html",
		                "userprofile/messages/send_confirm.text",
		                context,
		                settings.EMAIL_FROM_ADDRESS,
		                [user.username])

		note = _("Your activation link has been sent to your email address")
	data['note'] = note
	return render_to_response("userprofile/activate_resend.html", data, context_instance=RequestContext(request))

@login_required(login_url='/')
def password_reset(request):
	d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
	data = prepare_template_data(request)
	form = ChangePasswordForm()
	note = _("Change your password")
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			try:
				request.user.set_password(form.cleaned_data['password'])
				request.user.save()
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
	data = prepare_template_data(request)
	note = _("Please enter your registered email")
	if request.method == 'POST':
		try:
			user = User.objects.get(username=request.POST['email'])
			user_verification, created = UserVerification.objects.get_or_create(user_email=user.username)
			user_verification.password_reset_key = create_verification_link(user)
			user_verification.save()
			context = {}
			context['user'] = user
			context['activation_key'] = user_verification.password_reset_key
			domain = Site.objects.get(is_active=True).home_url
			if domain.endswith('/'):
				domain = domain.rstrip('/')
			context['domain'] = domain
	
			send_email("userprofile/messages/send_reset_password_key_subject.html",
							"userprofile/messages/send_reset_password_key.html",
							"userprofile/messages/send_reset_password_key.text",
							context,
							settings.EMAIL_FROM_ADDRESS,
							[user.username])
	
			note = _("""Password reset key has been sent""")
		except Exception as e:
			note = _("""Password reset operation failed""")
			log.error(e.message, extra=d)
	data['note'] = note
	return render_to_response("userprofile/change_password_key_request.html", data, context_instance=RequestContext(request))


def password_reset_key_done(request, key=None):
	d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
	data = prepare_template_data(request)
	note = _("Change your password")
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


def logout(request):
	logout_user(request)
	return HttpResponseRedirect("/")
