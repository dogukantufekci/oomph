from django.db import models
from django.conf import settings

class Word(models.Model):
    word = models.CharField(primary_key=True, max_length=100)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='words_created')
    to_learners = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='words_to_learn')
    learneders = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='words_learned')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.word