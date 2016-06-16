# -*- coding:utf-8  -*-

import random
from pysimplesoap.client import SoapClient

from abkayit.settings import TCKIMLIK_SORGULAMA_WS, EMAIL_FROM_ADDRESS



'''
    General operations that are used in userprofile app.
'''


class UserProfileOPS:
    def __init__(self):
        pass

    @staticmethod
    def generatenewpass(plen):
        chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijkmnpqrstuvwxyz'
        password = ''.join(random.choice(chars) for i in range(plen))
        return password

    @staticmethod
    def validateTCKimlikNo(tckimlikno, name, surname, year):
        try:
            client = SoapClient(wsdl=TCKIMLIK_SORGULAMA_WS, trace=False)
            response = client.TCKimlikNoDogrula(TCKimlikNo=tckimlikno,
                                                Ad=name.replace('i', 'İ').decode('utf-8').upper(),
                                                Soyad=surname.replace('i', 'İ').decode('utf-8').upper(), DogumYili=year)
            return response['TCKimlikNoDogrulaResult']
        except:
            return -1


