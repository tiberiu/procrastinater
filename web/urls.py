from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^procrastinater/', include('procrastinater.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),

    (r'^index/$', 'web.controllers.home.index'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    (r'^story/(?P<story_id>\d+)/$', 'web.controllers.story.view')
)
