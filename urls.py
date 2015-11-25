# -*- coding: utf-8 -*-
"""
Author  : Anshul Tiwari
Date    : Sep 30, 2015

Description : This holds the URL Description.
"""

from django.conf.urls.defaults import patterns, include, url
import rpc
import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from views.applauncher import AssetView

urlpatterns = patterns('',
    (r'^jsonrpc$', rpc.jsonrpc_handler),
    # Examples:

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #(r'^accounts/login/$',  'views.login_view'),
    (r'^accounts/login/$', 'views.login', {'template_name': 'login.html'}),
    (r'^accounts/logout/$', 'views.logout_view'),

    #url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^assetmanpage/$', AssetView.as_view()),
    url(r'^$', AssetView.as_view()),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT,
          'show_indexes': False}),

)
