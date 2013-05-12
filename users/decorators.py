from functools import wraps

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from users.models import User


def is_profile_public(fn):
    def inner_decorator(request, oomph_user):
        if not oomph_user.is_profile_public:
            if (
                request.user.is_anonymous() or 
                request.user not in oomph_user.followers.all() and 
                request.user.id != oomph_user.id
            ):
                return HttpResponse('Here.')
                return render(request, "users/blocked.html")
        # Proceed like normally with the request
        return fn(request, oomph_user)
    return wraps(fn)(inner_decorator)


def my_decorator(view_func):
    def _decorator(request, *args, **kwargs):
        return render(request, "users/blocked.html")
        response = view_func(request, *args, **kwargs)
        # maybe do something after the view_func call
        return response
    return wraps(view_func)(_decorator)