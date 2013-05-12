from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Site Index
    url(r'^$', 'activities.views.index'),

    # User
    url(r'^me/$', 'users.views.me_activities', name='me'),
    url(r'^me/activities/$', 'users.views.me_activities', name='me_activities'),
    url(r'^me/words-to-learn/$', 'users.views.me_words_to_learn', name='me_words_to_learn'),
    url(r'^me/words-learned/$', 'users.views.me_words_learned', name='me_words_learned'),
    url(r'^me/followers/$', 'users.views.me_followers', name='me_followers'),
    url(r'^me/following/$', 'users.views.me_following', name='me_following'),

    # Oomph Applications
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^activities/$', 'activities.views.index', name='activities'),
    url(r'^search/$', 'search.views.index', name='search'),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^words/', include('words.urls', namespace='words')),
)

# Serve static files
from django.conf import settings
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)