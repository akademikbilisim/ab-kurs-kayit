# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import signals
from abkayit.adaptor import send_email
from abkayit.models import Site
from userprofile.models import UserVerification
import random, hashlib

EMAIL_FROM_ADDRESS="kayit@ab.org.tr"

def send_confirm_link(sender, instance, created, **kwargs):
	if created:
		instance.is_active=False
		user_verification = UserVerification()
		user_verification.activation_key = create_verification_link(instance)
		user_verification.user_email=instance.username
		user_verification.save()
		data={}
		data['user'] = instance
		data['activation_key'] = user_verification.activation_key
		domain = Site.objects.get(is_active=True).home_url
		if domain.endswith('/'):
		 	domain = domain.rstrip('/')
		data['domain'] = domain
		send_email("userprofile/messages/send_confirm_subject.html",
						"userprofile/messages/send_confirm.html",
						"userprofile/messages/send_confirm.text",
						data,
						EMAIL_FROM_ADDRESS,
						[instance.username])
	

def create_verification_link(user):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    return hashlib.sha1(salt+user.username).hexdigest()


signals.post_save.connect(send_confirm_link, sender=User)
