#encoding=utf-8
# -*- coding: utf-8 -*-

from django.conf import settings

def debug(request):
    return {
        'debug': settings.DEBUG,
        'DEBUG': settings.DEBUG,
    }
