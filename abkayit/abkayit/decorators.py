#-*- coding:utf-8 -*-

def active_required(user):
	if not user.is_anonymous():
		if not user.is_active:
			return False
	return True
