# -*- coding: utf-8 -*-
import ConfigParser
from abkayit.settings import COMMON_CONFIG_FILE


class DBconfig:
    dbhost = None
    dbport = None
    database = None
    dbuser = None
    dbpass = None

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(COMMON_CONFIG_FILE)
        section = "DB"
        self.dbhost = config.get(section, "host")
        self.dbport = config.get(section, "port")
        self.database = config.get(section, "database")
        self.dbuser = config.get(section, "dbuser")
        self.dbpass = config.get(section, "pass")

    def getdbhost(self):
        return self.dbhost

    def getdbport(self):
        return self.dbport

    def getdatabase(self):
        return self.database

    def getdbuser(self):
        return self.dbuser

    def getdbpass(self):
        return self.dbpass


class LDAPconfig:
    ldaphost = None
    ldapport = None
    basedn = None
    ldappass = None
    searchdn = None

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(COMMON_CONFIG_FILE)
        section = "LDAP"
        self.ldaphost = config.get(section, "host")
        self.ldapport = config.get(section, "port")
        self.basedn = config.get(section, "basedn")
        self.ldappass = config.get(section, "pass")
        self.searchdn = config.get(section, "searchdn")

    def getldaphost(self):
        return self.ldaphost

    def getldapport(self):
        return self.ldapport

    def getbasedn(self):
        return self.basedn

    def getldappass(self):
        return self.ldappass

    def getsearchdn(self):
        return self.searchdn


class DjangoSettings:
    secret_key = None

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(COMMON_CONFIG_FILE)
        section = "DJANGO"
        self.secret_key = config.get(section, "secret_key")

    def getsecretkey(self):
        return self.secret_key


class EmailSettings:
    fromaddress = None
    host = None
    port = None

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(COMMON_CONFIG_FILE)
        section = "EMAIL"
        self.fromaddress = config.get(section, "from")
        self.host = config.get(section, "host")
        self.port = config.get(section, "port")


class SMSSettings:
    url = None
    usercode = None
    password = None
    msgheader = None

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(COMMON_CONFIG_FILE)
        section = "SMS"
        self.url = config.get(section, "url")
        self.usercode = config.get(section, "usercode")
        self.password = config.get(section, "password")
        self.msgheader = config.get(section, "msgheader")

    def get_url(self):
        return self.url

    def get_usercode(self):
        return self.usercode

    def get_password(self):
        return self.password

    def get_msgheader(self):
        return self.msgheader


class CaptchaSettings:
    publickey = None
    privatekey = None

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(COMMON_CONFIG_FILE)
        section = "CAPTCHA"
        self.publickey = config.get(section, 'publickey')
        self.privatekey = config.get(section, 'privatekey')

    def get_public_key(self):
        return self.publickey

    def get_private_key(self):
        return self.privatekey