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
