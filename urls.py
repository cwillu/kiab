from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Example:
  (r'^', include('kiab.contacts.urls')),

  # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
  # to INSTALLED_APPS to enable admin documentation:
  (r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  (r'^admin/(.*)', admin.site.root),
)

if not settings.PRODUCTION:
  urlpatterns += patterns(
    "django.views",
      url(r"%s(?P<path>.*)$" % settings.MEDIA_URL[1:], "static.serve", {
          "document_root": settings.MEDIA_ROOT,
      })
  )

