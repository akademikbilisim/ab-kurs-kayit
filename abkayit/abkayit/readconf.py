# -*- coding: utf-8 -*-
import ConfigParser
from .settings import COMMON_CONFIG_FILE


class DbConfig:
    db_host = None
    db_port = None
    database = None
    db_user = None
    db_pass = None

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(COMMON_CONFIG_FILE)

        section = "DB"
        self.db_host = config.get(section, "host")
        self.db_port = config.get(section, "port")
        self.database = config.get(section, "database")
        self.db_user = config.get(section, "db_user")
        self.db_pass = config.get(section, "pass")

    def get_db_host(self):
        return self.db_host

    def get_db_port(self):
        return self.db_port

    def get_database(self):
        return self.database

    def get_db_user(self):
        return self.db_user

    def get_db_pass(self):
        return self.db_pass


class DjangoSettings:
    secret_key = None

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(COMMON_CONFIG_FILE)
        section = "DJANGO"
        self.secret_key = config.get(section, "secret_key")

    def get_secret_key(self):
        return self.secret_key
