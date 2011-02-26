from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'^index/$', 'web.controllers.home.index'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    (r'^story/(?P<story_id>\d+)/$', 'web.controllers.story.view'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'web/static'})
)
