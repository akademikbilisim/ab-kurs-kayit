#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abkayit.settings")
    import sys
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(BASE_DIR, "abkayit"))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
