# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin

import cms
from cms.admin.placeholderadmin import PlaceholderAdmin

from models import TranslationRequest, TranslationResponse
import views


class TranslationRequestAdmin(admin.ModelAdmin):
    # readonly_fields = TranslationRequest._meta.get_all_field_names()

    def get_urls(self):
        urls = super(TranslationRequestAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'add/$', views.AddTranslationView.as_view(), name='add_translation'),
            url(r'select/(?P<pk>\d+)$', views.select_plugins_by_type_view, name='select_plugins_by_type'),
            url(r'quote/(?P<pk>\d+)$', views.get_quote_view, name='get_quote'),
            url(r'order/(?P<pk>\d+)$', views.order_view, name='order'),
            url(r'response/$', views.process_response, name='process_response'),
            # TODO: Add status view
        )

        return my_urls + urls
    pass


class TranslationResponseAdmin(admin.ModelAdmin):
    # readonly_fields = TranslationResponseAdmin._meta.get_all_field_names()
    pass


admin.site.register(TranslationRequest, TranslationRequestAdmin)
admin.site.register(TranslationResponse, TranslationResponseAdmin)
