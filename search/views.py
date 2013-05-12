from django.shortcuts import render

from users.models import User
from words.models import Word

def index(request):
    _filter = request.GET.get('group', '')
    query = request.GET.get('q', '')
    words = []
    oomph_users = []

    if _filter == 'words':
        words = Word.objects.order_by('?')[:10]
    elif _filter == 'users':
        oomph_users = User.objects.order_by('?')[:10]
    else:
        if query:
            words = Word.objects.filter(word__iexact=query)[:10]
            oomph_users = User.objects.filter(username__iexact=query)[:1]
        else:
            words = Word.objects.order_by('?').all()[:10]
            oomph_users = User.objects.order_by('?').all()[:10]

    perfect_match = None
    if query:
        try:
            perfect_match = Word.objects.get(word=query)
        except Word.DoesNotExist:
            pass

    user_following = []
    user_requesting_to_follow = []
    if oomph_users and request.user.is_authenticated():
        user_following = request.user.following.all()
        user_requesting_to_follow = request.user.requesting_to_follow.all()

    return render(request, "search/index.html", dict(
        (
            ('oomph_users', oomph_users),
            ('perfect_match', perfect_match),
            ('words', words),
            ('query', query),
            ('filter', _filter),
        ) + get_view_details(request)))


def get_view_details(request):
    user = (('user', request.user),)
    if request.user.is_authenticated():
        user = request.user.get_view_details()
    return user + (('current', request.get_full_path()),)