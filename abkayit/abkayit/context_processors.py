#!-*- coding:utf-8 -*-

import logging
from django.core.exceptions import *
from abkayit.models import Site

logger = logging.getLogger(__name__)


def template_data(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    site = None
    menus = []
    user = request.user
    try:
        site = Site.objects.get(is_active=True)
        menus = site.menu_set.order_by('order')
    except ObjectDoesNotExist:
        logger.error("active site not found", extra=d)
    return {'menus': menus, 'site': site, 'user': user}
