#!-*- coding:utf-8 -*-

import hashlib
import logging
import random
from django.core.exceptions import *
from abkayit.models import Site, Menu

log = logging.getLogger(__name__)


def getsiteandmenus(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    site = None
    menus = []
    try:
        site = Site.objects.get(is_active=True)
        menus = site.menu_set.order_by('order')
    except ObjectDoesNotExist:
        log.error("active site not found" % request.user, extra=d)
    return {'menus': menus, 'site': site, 'user': request.user}


def create_verification_link(user):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    return hashlib.sha1(salt + user.username).hexdigest()
