from django.core.mail import send_mail

from account.decorators import async

@async
def email_changed(user):
    message = """
    Dear %(username)s,
    
    You have changed your email address.
    Please verify your new email address by using this link:

    \thttp://pacific-springs-1995.herokuapp.com/account/settings/verify-email/?key=%(key)s

    Learn words with friends,
    Oomph
    """ % {
        'username': user.username,
        'key': user.email_verification_key
    }
    send_mail('Your email has been changed.',
              message, 
              'labs@creco.co', 
              [user.email], 
              fail_silently=False)