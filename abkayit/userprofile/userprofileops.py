# -*- coding:utf-8  -*-

import random
'''
    General operations that are used in userprofile app.
'''

class UserProfileOPS():
	def createUserFormIsValid(self,postrequest):
		not_valid_fields=[]
		if not postrequest['first_name']:
			not_valid_fields.append("Ad alani bos olamaz!")
		if not postrequest['last_name']:
			not_valid_fields.append("Soyad alani bos olamaz!")
		if not postrequest['email']:
			not_valid_fields.append("E-posta alani bos olamaz!")
		if not postrequest['password']:
			not_valid_fields.append("Parola alani bos olamaz!")
		else:
			if not postrequest['passwordre']:
				not_valid_fields.append("Parola Dogrulama alani bos olamaz!")
			elif postrequest['passwordre']!=postrequest['password']:
				not_valid_fields.append("Parola ve Parola Dogrulama alanlari ayni olmali!")
		return not_valid_fields
	def usercreatePostDataToDict(self,postrequest):
		data={}
		for key in postrequest:
			if key is not "username":
				data[key]=postrequest[key]
		data['username']=postrequest['email']
		return data
	def generatenewpass(self,plen):
		chars='ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijkmnpqrstuvwxyz'
		password=''.join(random.choice(chars) for i in range(plen))
		return password
