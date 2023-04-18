# used for authentication
from django.contrib.auth.models import User
# django signal pre and post action
from django.db.models.signals import post_save, post_delete
# decorator
from django.dispatch import receiver
# importing Profile module
from .models import Profile
# mail
from django.core.mail import send_mail
# importing settings.py
from django.conf import settings

# signal
# @receiver(post_save, sender=Profile)


# created can be true if first time created
def createUpdated(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(  # when we create user then automatically profile is created
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = 'Welcome to IP-Jugadd Projects...'
        message = 'Hi\nI am Manish Kumar. Thanks for Siging Up You are joining our community.\nBest...'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )
# by updating profile user also get update


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user  # coz it's one to one
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# when we delete profile user should also get deleted
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createUpdated, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
