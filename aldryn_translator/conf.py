# -*- coding: utf-8 -*-
from django.conf import settings
from appconf import AppConf


class AldrynTemplateAppConf(AppConf):
    PLUGIN_LANGUAGE = settings.LANGUAGES[0][0]

    class Meta:
        prefix = 'ALDRYN_TRANSLATOR'
