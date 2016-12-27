from rest_framework import serializers
from Accounts.models import User

__author__ = 'Pratick'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
