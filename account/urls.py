from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^register/$', 'account.views.register', name='register'),
    url(r'^login/$', 'account.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    url(r'^settings/$', 'account.views.settings', name='settings'),
    url(r'^settings/verify-email/$', 'account.views.settings_verify_email', name='settings_verify_email'),
)