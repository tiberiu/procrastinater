from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'web.controllers.index.index'),
    (r'^index/(?P<id>\d*)$', 'web.controllers.index.index'),
    (r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^profile/$', 'web.controllers.profile.edit'),
    (r'^profile/save$', 'web.controllers.profile.save'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'web/static'})
)
