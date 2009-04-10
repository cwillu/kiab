from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^contact/create', views.createContact),
    (r'^contact/(.*)/', views.contact),
    (r'^contact/(.*)/update', views.update),
    (r'^contact/(.*)/comment', views.comment),
)
