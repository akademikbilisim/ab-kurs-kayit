# -*- coding:utf-8  -*-

import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from abkayit.models import *
from abkayit.backend import prepare_template_data

log = logging.getLogger(__name__)

def index(request):
	d = {'clientip': request.META['REMOTE_ADDR'], 'user':request.user}
	data = prepare_template_data(request)
	content = None
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


