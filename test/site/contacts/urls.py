# encoding=utf-8
from django.conf.urls import url
from django.conf.urls import include
# from django.contrib.auth.models import User

# from rest_framework import routers, serializers, viewsets

# from .models import Contact

import contacts.views as views

app_name = 'contacts'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<id>\d+)/$', views.read, name='read'),
    url(r'^(?P<id>\d+)/update/$', views.update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', views.delete, name='delete'),

    url(r'^all/delete/$', views.delete_all, name='delete_all'),
    url(r'^create/all/$', views.generate, name='generate'),

    url(r'^export/csv/$', views.export_csv, name='export_csv'),
    url(r'^export/json/$', views.export_json, name='export_json'),

    url(r'^import/$', views.import_index, name='import'),
]
