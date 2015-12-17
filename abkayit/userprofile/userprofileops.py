# -*- coding:utf-8  -*-

import random
from pysimplesoap.client import SoapClient

'''
    General operations that are used in userprofile app.
'''

class UserProfileOPS():
	def generatenewpass(self,plen):
		chars='ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijkmnpqrstuvwxyz'
		password=''.join(random.choice(chars) for i in range(plen))
		return password
	def validateTCKimlikNo(self, tckimlikno, name, surname, year):
		try:
			client = SoapClient(wsdl="https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL", trace=False)
			response = client.TCKimlikNoDogrula(TCKimlikNo=tckimlikno, Ad=name.replace('i', 'İ').decode('utf-8').upper(), Soyad=surname.replace('i', 'İ').decode('utf-8').upper(), DogumYili=year)
			return response['TCKimlikNoDogrulaResult']
		except:
			return -1
