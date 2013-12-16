# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from aldryn_translator import views


urlpatterns = patterns('',
    url(r'add/$', views.AddTranslationView.as_view(), name='add_translation'),
    url(r'select/(?P<pk>\d+)$', views.select_plugins_by_type_view, name='select_plugins_by_type'),
    url(r'quote/(?P<pk>\d+)$', views.get_quote_view, name='get_quote'),
    url(r'order/(?P<pk>\d+)$', views.order_view, name='order'),
    url(r'response/$', views.process_response, name='process_response'),

)
