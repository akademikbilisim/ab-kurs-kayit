# -*- coding:utf-8  -*-
import logging
import random
import string
from abkayit.settings import TCKIMLIK_SORGULAMA_WS
from pysimplesoap.client import SoapClient

'''
    General operations that are used in userprofile app.
'''

logger = logging.getLogger(__name__)


class UserProfileOPS():
    def generate_new_pass(self, plen):
        return ''.join(
            random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(plen))


    @staticmethod
    def validate_tckimlik_no(tckimlikno, name, surname, year):
        try:
            client = SoapClient(wsdl=TCKIMLIK_SORGULAMA_WS, trace=False)
            response = client.TCKimlikNoDogrula(TCKimlikNo=tckimlikno,
                                                Ad=name.replace('i', 'İ').decode('utf-8').upper(),
                                                Soyad=surname.replace('i', 'İ').decode('utf-8').upper(), DogumYili=year)
            return response['TCKimlikNoDogrulaResult']
        except Exception as e:
            logger.error("it couldn't validated", e.message)
            return -1
