#!-*- coding:utf-8 -*-

import hashlib
import logging
import random
from django.core.exceptions import *
from abkayit.models import Site, Menu

log = logging.getLogger(__name__)

def create_verification_link(user):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    return hashlib.sha1(salt + user.username).hexdigest()
