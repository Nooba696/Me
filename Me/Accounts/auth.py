from django.db.models import Q
from Accounts.models import User

__author__ = 'Pratick'


class AuthBackend(object):

    def authenticate(self, username=None, password=None):

        try:
            user = self.get_user(username)
            print(password)
            print(user.check_password(password))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            try:
                user = User.objects.get(
                    Q(id=user_id)
                )
            except:
                user = User.objects.get(
                    Q(username=user_id) | Q(email=user_id) | Q(phone=user_id)
                )
            return user
        except User.DoesNotExist:
            return None