from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
from rest_framework.authtoken.models import Token
from Accounts.managers import UserManager
from Accounts.utils import phone_regex


class User(AbstractBaseUser, PermissionsMixin):
    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        if self.username:
            return self.username
        elif self.email:
            return self.email
        else:
            return self.phone

    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    phone = models.CharField(validators=[phone_regex], unique=True, null=True, max_length=15, blank=True)
    first_name = models.CharField(max_length=15, null=True, blank=True)
    last_name = models.CharField(max_length=15, null=True, blank=True)
    is_staff = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)




