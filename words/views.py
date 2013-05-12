from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse

from words.forms import WordForm
from words.models import Word
from activities.choices import ActivityVisibilityChoices, ActivityTypeChoices

db = settings.MONGODB

def word(request, word):
    word = get_object_or_404(Word, word=word)
    return render(request, "words/word.html", {
        'user': request.user,
        'word': word,
        'current': request.get_full_path(),
        'user_words_learned': request.user.words_learned.all(),
        'user_words_to_learn': request.user.words_to_learn.all(),
    })

def index(request):
    if request.user.is_anonymous() or request.method != 'POST':
        return HttpResponseRedirect('/search/?group=words')

    form = WordForm(request.POST)
    if form.is_valid():
        word = Word(
            word=form.cleaned_data['word'],
            creator=request.user
        )
        word.save()
        if request.user.is_words_created_public and request.user.is_profile_public:
            visibility = ActivityVisibilityChoices.PUBLIC
        elif request.user.is_words_created_public and not request.user.is_profile_public:
            visibility = ActivityVisibilityChoices.LIMITED
        else:
            visibility = ActivityVisibilityChoices.PRIVATE

        db.activities.insert({
            'user': {
                'username': request.user.username,
                'id': request.user.id,
                'facebook_id': request.user.facebook_id,
            },
            'type': ActivityTypeChoices.CREATED_WORD,
            'word': word.word,
            'created_at': datetime.utcnow(),
            'visibility': visibility
        })
        return HttpResponseRedirect(reverse('words:word', args=(word.word,)))
    return HttpResponseRedirect('/search/?group=words')