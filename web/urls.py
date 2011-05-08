from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    url(r'^$', 'web.controllers.index.index', name="index"),

    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
        name="logout"),
    url(r'^profile/$', 'web.controllers.profile.edit',
        name="profile_edit"),
    url(r'^profile/save$', 'web.controllers.profile.save',
        name="profile_save"),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'web/static'}, name="static_file")
)
