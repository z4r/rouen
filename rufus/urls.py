from django.conf.urls.defaults import *

urlpatterns = patterns('rufus.views',
                           (r'^export/(?P<command>provider|service)/$','export'),
                      )
