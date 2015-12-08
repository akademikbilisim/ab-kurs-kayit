# -*- coding:utf-8  -*-
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

from userprofile.forms import CreateUserForm, InstProfileForm
from userprofile.models import SubscribeNotice

from abkayit.models import *
from abkayit.settings import USER_TYPES
from abkayit.backend import prepare_template_data

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
	return HttpResponseRedirect('/')

def subscribe(request):
	data = prepare_template_data(request)	
	if not request.user.is_authenticated():
		note = _("Register to system to give training,  participation in courses before the conferences, and  participation in conferences.")
		form = CreateUserForm()
		if request.method == 'POST':
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
					print e.message
		data['createuserform']=form
		data['note']=note
			
		return render_to_response("userprofile/subscription.html",data,context_instance=RequestContext(request))
	else:
		return redirect("controlpanel")


def logout(request):
	logout_user(request)
	return HttpResponseRedirect("/")
