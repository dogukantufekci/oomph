from django import forms
from django.utils.translation import ugettext_lazy as _

from words.models import Word

class WordForm(forms.Form):
    word = forms.RegexField(
        regex=r'^[-A-Za-z0-9_.]+$',
        max_length=100,
        widget=forms.TextInput(),
        label=_("Word"),
        error_messages={'invalid': _("This value must contain only letters, "
                                     "numbers, hypens, dots and underscores.")})

    def clean_word(self):
        try:
            word = Word.objects.get(word=self.cleaned_data['word'])
        except Word.DoesNotExist:
            return self.cleaned_data['word']
        raise forms.ValidationError(_("%s is already added." % self.cleaned_data['word']))