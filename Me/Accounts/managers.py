from django.utils import timezone

__author__ = 'Pratick'

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, username=None, email=None, phone=None, first_name=None, last_name=None, password1=None, password2=None, is_staff=False):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email and not phone and not username:
            raise ValueError('Email or Phone or Username must be set')

        if password1 != password2:
            raise ValueError('Passwords Do Not Match')
        
        if email:
            email = self.normalize_email(email)

        user = self.model(username=username,
                          email=email,
                          phone=phone,
                          first_name=first_name,
                          last_name=last_name,
                          is_staff=is_staff,
                          is_superuser=is_staff,
                          is_active=True,
                          last_login=now,
                          date_joined=now)

        user.set_password(password1)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, phone=None, first_name=None, last_name=None, password1=None, password2=None):
        return self._create_user(username, email, phone, first_name, last_name, password1, password2, False)

    def create_superuser(self, username=None, email=None, phone=None, first_name=None, last_name=None, password=None):
        return self._create_user(username, email, phone, first_name, last_name, password, password, True)