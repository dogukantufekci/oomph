from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'words.views.index', name='index'),
    url(r'^(?P<word>[-A-Za-z0-9_.]+)/$', 'words.views.word', name='word'),
)