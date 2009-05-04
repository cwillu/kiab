from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^contact/create/$', views.blankContact),
    (r'^contact/search/(.*?)$', views.search),
    (r'^contact/(.*?)/$', views.showContact),
    (r'^contact/(.*?)/updateDetail$', views.updateDetail),
    (r'^contact/(.*?)/updateName$', views.updateName),
    (r'^contact/(.*?)/addComment$', views.addComment),
)
