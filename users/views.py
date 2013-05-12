from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required

from activities.choices import ActivityVisibilityChoices, ActivityTypeChoices
from users.models import User
from words.models import Word

db = settings.MONGODB


def index(request):
    return HttpResponseRedirect('/search/?group=users')


def user_activities(request, username):
    oomph_user = get_object_or_404(User, username=username)
    if not verify_view_access(request, request.user, oomph_user):
        return render(request, "users/view_access_denied.html", dict(
            get_view_details(request, oomph_user))
        )

    if oomph_user == request.user:
        query = {'user.id': request.user.id}
    elif (
        request.user.is_authenticated() and
        request.user in oomph_user.followers.all()
    ):
        query = {
            'visibility': {'$ne': ActivityVisibilityChoices.PRIVATE},
            'user.id': oomph_user.id
        }
    else:
        query = {
            'visibility': ActivityVisibilityChoices.PUBLIC,
            'user.id': oomph_user.id
        }

    activities = list(db.activities.find(query).sort('created_at', -1).limit(10))
    return render(request, "users/user-activities.html", dict(
        (
            ('activities', activities),
        ) + get_view_details(request, oomph_user)))


def user_words_to_learn(request, username):
    if (
        request.method == 'POST' and
        request.user.is_authenticated()
    ):
        word_to_learn = request.POST.get('word_to_learn')
        if word_to_learn is not None:
            word_to_learn = get_object_or_404(Word, word=word_to_learn)
            if request.POST.get('method') == 'DELETE':
                request.user.words_to_learn.remove(word_to_learn)
                request.user.save()
            else:
                request.user.words_to_learn.add(word_to_learn)
                request.user.save()

                if request.user.is_words_to_learn_public and request.user.is_profile_public:
                    visibility = ActivityVisibilityChoices.PUBLIC
                elif request.user.is_words_to_learn_public and not request.user.is_profile_public:
                    visibility = ActivityVisibilityChoices.LIMITED
                else:
                    visibility = ActivityVisibilityChoices.PRIVATE

                db.activities.insert({
                    'user': {
                        'username': request.user.username,
                        'id': request.user.id,
                        'facebook_id': request.user.facebook_id,
                    },
                    'type': ActivityTypeChoices.ADDED_WORD_TO_LEARN,
                    'word': word_to_learn.word,
                    'created_at': datetime.utcnow(),
                    'visibility': visibility
                })

    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET['next'])

    oomph_user = get_object_or_404(User, username=username)

    if not verify_view_access(request, request.user, oomph_user):
        return render(request, "users/view_access_denied.html", dict(
            get_view_details(request, oomph_user))
        )

    return render(request, "users/user-words-to-learn.html", dict(
        (
            ('oomph_user_words_to_learn', oomph_user.words_to_learn.all()),
        ) + get_view_details(request, oomph_user)))


def user_words_learned(request, username):
    if (
        request.method == 'POST' and
        request.user.is_authenticated()
    ):
        word_learned = request.POST.get('word_learned')
        if word_learned is not None:
            word_learned = get_object_or_404(Word, word=word_learned)
            if request.POST.get('method') == 'DELETE':
                request.user.words_learned.remove(word_learned)
                request.user.save()
            else:
                request.user.words_learned.add(word_learned)
                request.user.save()

                if request.user.is_words_learned_public and request.user.is_profile_public:
                    visibility = ActivityVisibilityChoices.PUBLIC
                elif request.user.is_words_learned_public and not request.user.is_profile_public:
                    visibility = ActivityVisibilityChoices.LIMITED
                else:
                    visibility = ActivityVisibilityChoices.PRIVATE

                db.activities.insert({
                    'user': {
                        'username': request.user.username,
                        'id': request.user.id,
                        'facebook_id': request.user.facebook_id,
                    },
                    'type': ActivityTypeChoices.ADDED_WORD_LEARNED,
                    'word': word_learned.word,
                    'created_at': datetime.utcnow(),
                    'visibility': visibility
                })

    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET['next'])

    oomph_user = get_object_or_404(User, username=username)

    if not verify_view_access(request, request.user, oomph_user):
        return render(request, "users/view_access_denied.html", dict(
            get_view_details(request, oomph_user))
        )


    return render(request, "users/user-words-learned.html", dict(
        (
            ('oomph_user_words_learned', oomph_user.words_learned.all()),
        ) + get_view_details(request, oomph_user)))


def user_followers(request, username):
    oomph_user = get_object_or_404(User, username=username)
    if not verify_view_access(request, request.user, oomph_user):
        return render(request, "users/view_access_denied.html", dict(
            get_view_details(request, oomph_user))
        )


    return render(request, "users/user-followers.html", dict(
        (
            ('oomph_user_followers', oomph_user.followers.all()),
        ) + get_view_details(request, oomph_user)))


def user_following(request, username):
    oomph_user = get_object_or_404(User, username=username)

    if (
        request.method == 'POST' and
        request.user.is_authenticated() and
        request.user == oomph_user
    ):
        
        followed_user_id = int(request.POST.get('followed_user_id'))
        if followed_user_id is not None:
            followed_user = get_object_or_404(User, pk=followed_user_id)

            if request.POST.get('method') == 'POST':

                if followed_user.is_profile_public:
                    request.user.following.add(followed_user)
                    request.user.save()
                else:
                    request.user.requesting_to_follow.add(followed_user)
                    request.user.save()

            elif request.POST.get('method') == 'DELETE':

                if followed_user_id is not None: 
                    followed_user = get_object_or_404(User, pk=followed_user_id)
                    request.user.following.remove(followed_user)
                    request.user.requesting_to_follow.remove(followed_user)
                    request.user.save()

    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET['next'])

    if not verify_view_access(request, request.user, oomph_user):
        return render(request, "users/view_access_denied.html", dict(
            get_view_details(request, oomph_user))
        )

    return render(request, "users/user-following.html", dict(
        (
            ('oomph_user_following', oomph_user.following.all()),
        ) + get_view_details(request, oomph_user)))


def verify_view_access(request, user, oomph_user):
    if oomph_user.is_profile_public:
        pass
    elif user.is_anonymous() or (
        user != oomph_user and
        user not in oomph_user.followers.all()
    ):
        return False
    return True


def get_view_details(request, oomph_user):
    user = (('user', request.user),)
    if request.user.is_authenticated():
        user = request.user.get_view_details()
    return user + (('oomph_user', oomph_user), ('current', request.get_full_path()))


# Me -------------------------------------------------------------------------


@login_required
def me_activities(request):
    return user_activities(request=request, username=request.user.username)


@login_required
def me_words_to_learn(request):
    return user_words_to_learn(request=request, username=request.user.username)


@login_required
def me_words_learned(request):
    return user_words_learned(request=request, username=request.user.username)


@login_required
def me_followers(request):
    return user_followers(request=request, username=request.user.username)


@login_required
def me_following(request):
    return user_following(request=request, username=request.user.username)