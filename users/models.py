from random import random
from hashlib import md5

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email_verification_key = models.CharField(max_length=32, null=True)
    facebook_id = models.BigIntegerField(null=True)
    is_profile_public = models.BooleanField(default=True)
    is_words_created_public = models.BooleanField(default=True)
    is_words_to_learn_public = models.BooleanField(default=True)
    is_words_learned_public = models.BooleanField(default=True)
    requesting_to_follow = models.ManyToManyField('self', symmetrical=False, related_name='users_requesting_to_follow_me')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def get_view_details(self):
        return (
            ('user', self),
            ('user_words_to_learn', self.words_to_learn.all()),
            ('user_words_learned', self.words_learned.all()),
            ('user_following', self.following.all()),
            ('user_requesting_to_follow', self.requesting_to_follow.all()),
        )

    def verify_email(self, email_verification_key):
        if self.email_verification_key == email_verification_key:
            self.email_verification_key = None
            self.save()
            return True
        return False

    @staticmethod
    def generate_email_verification_key(email):
        return md5(str(random()) + str(email)).hexdigest()