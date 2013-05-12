from django import forms
from django.utils.translation import ugettext_lazy as _

from users.models import User


class RegisterForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(),
                                label=_("Username"),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(max_length=75,
                             widget=forms.TextInput(),
                             label=_("Email"))
    password1 = forms.CharField(min_length=6,
                                widget=forms.PasswordInput(render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("Password (again)"))
    
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_email(self):
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("A user with that email address already exists."))

    def clean_password2(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data['password2']


class LoginForm(forms.Form):
    email = forms.CharField(max_length=75,
                            widget=forms.TextInput(attrs={'placeholder': 'Email or username'}),
                            label=_("Email"))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               label=_("Password"))


class SettingsForm(forms.Form):
    username = forms.RegexField(
        regex=r'^\w+$',
        max_length=30,
        widget=forms.TextInput(),
        label=_("Username"),
        error_messages={'invalid': _("This value must contain only letters, "
                                     "numbers and underscores.")}
    )
    email = forms.EmailField(
        max_length=75,
        widget=forms.TextInput(),
        label=_("Email")
    )
    facebook_id = forms.IntegerField(
        required=False,
        label=_("Facebook ID (For Picture)")
    )
    is_profile_public = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label=_("Profile")
    )
    is_words_created_public = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label=_("Words Created")
    )
    is_words_to_learn_public = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label=_("Words To-Learn")
    )
    is_words_learned_public = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label=_("Words Learned")
    )

    user = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SettingsForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        if self.user.username.lower() == self.cleaned_data['username'].lower():
            return self.cleaned_data['username']
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_email(self):
        if self.user.email.lower() == self.cleaned_data['email'].lower():
            return self.cleaned_data['email']
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("A user with that email address already exists."))