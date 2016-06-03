# -*- coding: utf-8 -*-
import datetime


class DynmcFields:
    BirthDateYears = None

    def __init__(self):
        now = datetime.datetime.now()
        curyear = now.year
        self.BirthDateYears = ()
        for i in range(100):
            self.BirthDateYears += (str(curyear - (i + 2)),)
