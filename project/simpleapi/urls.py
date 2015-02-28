from django.conf.urls import patterns, include, url
from django.contrib import admin


import school.views

urlpatterns = patterns('',
    url(r'^(xml|json)/auth/', school.views.AuthRestToken.as_view(), name='auth-by-token'),
    url(r'^(xml|json)/query/', school.views.QuaryHandler.as_view(), name='query-data'),
)
