#!-*- coding:utf-8 -*-

from abkayit.models import Menu

def prepare_template_data(request):
	pages = Menu.objects.filter(site__is_active=True).order_by('order')
	site = pages.first().site
	user = request.user
	return {'pages':pages, 'site':site, 'user':user}

