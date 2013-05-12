from oomph.choices import Choices
    
class ActivityTypeChoices(Choices):
    CREATED_USER = 1
    DELETED_USER = -1
    CREATED_WORD = 2
    DELETED_WORD = -2
    ADDED_WORD_TO_LEARN = 3
    REMOVED_WORD_TO_LEARN = -3
    ADDED_WORD_LEARNED = -4
    REMOVED_WORD_LEARNED = -4
    FOLLOWED_USER = 6
    UNFOLLOWED_USER = -6

class ActivityVisibilityChoices(Choices):
    PUBLIC = 1
    LIMITED = 2
    PRIVATE = 3