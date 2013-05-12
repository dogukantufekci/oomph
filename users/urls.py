from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'users.views.index', name='index'),
    url(r'^(?P<username>\w+)/$', 'users.views.user_activities', name='user'),
    url(r'^(?P<username>\w+)/activities/$', 'users.views.user_activities', name='user_activities'),
    url(r'^(?P<username>\w+)/words-to-learn/$', 'users.views.user_words_to_learn', name='user_words_to_learn'),
    url(r'^(?P<username>\w+)/words-learned/$', 'users.views.user_words_learned', name='user_words_learned'),
    url(r'^(?P<username>\w+)/followers/$', 'users.views.user_followers', name='user_followers'),
    url(r'^(?P<username>\w+)/following/$', 'users.views.user_following', name='user_following'),
)