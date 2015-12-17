#!-*- coding:utf-8 -*-

import random, hashlib
from abkayit.models import Menu

def prepare_template_data(request):
	pages = Menu.objects.filter(site__is_active=True).order_by('order')
	site = pages.first().site
	user = request.user
	return {'pages':pages, 'site':site, 'user':user}

def create_verification_link(user):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    return hashlib.sha1(salt+user.username).hexdigest()

