from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django import forms

from account.forms import RegisterForm, LoginForm, SettingsForm
from account.emails import email_changed
from users.models import User

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password2']
            )
            user.email_verification_key = User.generate_email_verification_key(user.email)
            user.save()
            user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password2'])
            auth.login(request, user)
            return HttpResponseRedirect(reverse('me'))
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if '@' not in form.cleaned_data['email']:
                username = form.cleaned_data['email']
            else:
                try:
                    user = User.objects.get(email=form.cleaned_data['email'])
                    username = user.username
                except User.DoesNotExist:
                    username = None
            if username is not None:
                user = auth.authenticate(username=username, 
                                         password=form.cleaned_data['password'])
                if user is not None:
                    if user.is_active:
                        auth.login(request, user)
                        return HttpResponseRedirect(request.GET.get('next') or reverse('me'))
            messages.error(request, "Your email and password didn't match. Please try again.")
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {
        'form': form,
        'next': request.GET.get('next', '')
    })

@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = SettingsForm(request.POST, user=user)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            if user.email != form.cleaned_data['email']:
                user.email = form.cleaned_data['email']
                user.email_verification_key = User.generate_email_verification_key(user.email)
                email_changed(user)
            user.facebook_id = form.cleaned_data['facebook_id']
            if (
                user.is_profile_public != form.cleaned_data['is_profile_public'] and
                form.cleaned_data['is_profile_public']
            ):
                transfer_users_requesting_to_follow_me_to_followers(user)
            user.is_profile_public = form.cleaned_data['is_profile_public']
            user.is_words_created_public = form.cleaned_data['is_words_created_public']
            user.is_words_to_learn_public = form.cleaned_data['is_words_to_learn_public']
            user.is_words_learned_public = form.cleaned_data['is_words_learned_public']
            user.save()
            messages.success(request, "Settings has been updated.")
            return HttpResponseRedirect(reverse('account:settings'))
    else:
        form = SettingsForm(user=user, initial={
            'username': user.username,
            'email': user.email,
            'facebook_id': user.facebook_id,
            'is_profile_public': user.is_profile_public,
            'is_words_created_public': user.is_words_created_public,
            'is_words_to_learn_public': user.is_words_to_learn_public,
            'is_words_learned_public': user.is_words_learned_public
        })
    return render(request, "account/settings.html", {'form': form, 'user': request.user})

@login_required
def settings_verify_email(request):
    if not request.user.email_verification_key:
        messages.info(request, "You have already verified your email address.")
    elif request.GET.get('key'):
        if request.user.verify_email(request.GET['key']):
            messages.success(request, "Your email has been verified.")
        else:
            messages.error(request, "Email verification key is not valid.")
    else:
        messages.error(request, "No email verification key was detected.")

    return HttpResponseRedirect(reverse('account:settings'))


# functions -----------------------------------------------------------------

def transfer_users_requesting_to_follow_me_to_followers(user):
    for _user in user.users_requesting_to_follow_me.all():
        user.followers.add(_user)
    user.users_requesting_to_follow_me.clear()
    user.save()