import datetime

from django import template
from django.utils.timezone import utc

from activities.choices import ActivityTypeChoices

register = template.Library()

@register.filter(name='type')
def type(_type):
    if _type == ActivityTypeChoices.CREATED_USER:
        type_string = "registered Oomph"
    elif _type == ActivityTypeChoices.DELETED_USER:
        type_string = "quit Oomph"
    elif _type == ActivityTypeChoices.CREATED_WORD:
        type_string = "created a new word"
    elif _type == ActivityTypeChoices.DELETED_WORD:
        type_string = "deleted a word"
    elif _type == ActivityTypeChoices.ADDED_WORD_TO_LEARN:
        type_string = "added a word to Words To-Learn"
    elif _type == ActivityTypeChoices.REMOVED_WORD_TO_LEARN:
        type_string = "removed a word from Words To-Learn"
    elif _type == ActivityTypeChoices.ADDED_WORD_LEARNED:
        type_string = "added a word to Words Learned"
    elif _type == ActivityTypeChoices.REMOVED_WORD_LEARNED:
        type_string = "removed a word from Words Learned"
    elif _type == ActivityTypeChoices.FOLLOWED_USER:
        type_string = "started following a user"
    elif _type == ActivityTypeChoices.UNFOLLOWED_USER:
        type_string = "stopped following a user"
    else:
        type_string = "did an unknown activity"

    return type_string

@register.filter(name='age')
def age(created_at):
    now = datetime.datetime.utcnow()
    age_in_minutes = int((now - created_at).total_seconds())/60

    if age_in_minutes < 60:
        value = age_in_minutes
        precision = 'minute'
    elif age_in_minutes < 60*24:
        value = age_in_minutes // 60
        precision = 'hour'
    else:
        value = age_in_minutes // (60*24)
        precision = 'day'

    age_string = '%d %s%s ago' % (value, precision, ('s' if value > 1 else ''))
    return age_string