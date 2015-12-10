# -*- coding:utf-8  -*-
from django.http.response import HttpResponseRedirect
from abkayit.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.core.exceptions import ObjectDoesNotExist

def index(request):
	site=Site.objects.get(is_active=True)
	if request.GET.get('menu'):
		menu = request.GET.get('menu')
	else:
		try:
 			menu = Menu.objects.get(site=site.pk, name="Anasayfa").id
		except ObjectDoesNotExist:
			pass
	pages=Menu.objects.filter(site=site.pk).order_by('order')
	try:
		content = Content.objects.get(menu=menu)
	except ObjectDoesNotExist:
		content = None
	return render_to_response('dashboard.html',{'site':site,'pages':pages,'user':request.user, 'content':content})	
