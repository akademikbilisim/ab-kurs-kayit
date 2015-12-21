# -*- coding:utf-8  -*-

import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate,login
from abkayit.models import *
from abkayit.backend import prepare_template_data

log = logging.getLogger(__name__)
@csrf_exempt
def index(request):
	d = {'clientip': request.META['REMOTE_ADDR'], 'user':request.user}
	data = prepare_template_data(request)
	content = None
	data['state']=""
	if not request.user.is_authenticated():
		data['alerttype'] = "alert-info"
		data['state']=_("If you already have an account, please login from top right hand side of the page")
		if request.POST:
			username=request.POST['username']
			password=request.POST['password']
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
				log.info("%s user successfuly logged in" % (request.user), extra=d)
				return HttpResponseRedirect('/')
			else:
				data['state']=_("Login Failed!")
				data['alerttype'] = "alert-danger"
	try:
		if not request.GET.get('menu_id'):
			menu_id = Menu.objects.all().order_by('order').first()
		else:
			menu_id = request.GET.get('menu_id')
		content = Content.objects.get(menu=menu_id)
	except ObjectDoesNotExist:
		content = None
		log.error("%s entered content not found " % (request.user), extra=d)
	except Exception as e:
		log.error("%s error occured %s " % (request.user, e.message), extra=d)
	data['content'] = content
	return render_to_response('dashboard.html', data)


