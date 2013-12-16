# -*- coding: utf-8 -*-
from django.contrib import admin

import cms
from cms.admin.placeholderadmin import PlaceholderAdmin

from models import TranslationRequest, TranslationResponse


class TranslationRequestAdmin(admin.ModelAdmin):
    # readonly_fields = TranslationRequest._meta.get_all_field_names()
    pass


class TranslationResponseAdmin(admin.ModelAdmin):
    # readonly_fields = TranslationResponseAdmin._meta.get_all_field_names()
    pass


admin.site.register(TranslationRequest, TranslationRequestAdmin)
admin.site.register(TranslationResponse, TranslationResponseAdmin)
