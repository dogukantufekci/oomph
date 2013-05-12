from django.shortcuts import render
from django.conf import settings

from activities.choices import ActivityVisibilityChoices
from words.models import Word

db = settings.MONGODB

def index(request):
    filter_status = {
        'public': 'inactive',
        'friends': 'inactive',
        'me': 'inactive'
    }
    user_words_to_learn = []

    if request.user.is_anonymous():
        query = {'visibility': ActivityVisibilityChoices.PUBLIC}
        filter_status['public'] = 'active'
        suggested_word = None
    else:
        suggested_word = Word.objects.order_by('?').all()[0]
        user_words_to_learn = request.user.words_to_learn.order_by('created_at')[:10]
        if request.GET.get('filter') == 'friends':
            following = [user.id for user in request.user.following.all()]
            query = {'$or': [
                {'user.id': request.user.id},
                {
                    'visibility': {'$ne': ActivityVisibilityChoices.PRIVATE},
                    'user.id': {'$in': following}
                }
            ]}
            filter_status['friends'] = 'active'
        elif request.GET.get('filter') == 'me':
            query = {'user.id': request.user.id}
            filter_status['me'] = 'active'
        else:
            query = {'visibility': ActivityVisibilityChoices.PUBLIC}
            filter_status['public'] = 'active'

    activities = list(db.activities.find(query).sort('created_at', -1).limit(10))
    return render(request, "activities/index.html", {
        'user': request.user,
        'activities': activities,
        'suggested_word': suggested_word,
        'user_words_to_learn': user_words_to_learn,
        'filter_status': filter_status,
    })