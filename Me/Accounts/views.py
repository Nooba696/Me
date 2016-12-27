# Create your views here.
from django.contrib.auth.hashers import make_password
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from Accounts.auth import AuthBackend
from Accounts.models import User
from Accounts.serializers import UserSerializer


class UserView(APIView):
    permission_classes = {permissions.IsAuthenticated}

    def get(self, request, pk):

        user = AuthBackend().get_user(user_id=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def put(self, request, pk):

        user = AuthBackend().authenticate(username=pk, password=request.data.get('password'))

        if user is None:
            raise ValueError('User could not be authenticated')

        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():

            if request.data.get('new_password'):
                serializer.validated_data['password'] = make_password(request.data['new_password'])
            else:
                serializer.validated_data['password'] = make_password(request.data['password'])
            serializer.save()
            print(serializer.data)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        try:

            user = AuthBackend().authenticate(username=pk, password=request.data.get('password'))
            if user is None:
                raise ValueError('User could not be authenticated')
            user.delete()

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        phone = request.data.get('phone')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        if password1 is None or password2 is None:
            raise ValueError('Invalid Password')

        user = User.objects.create_user(username, email, phone, first_name, last_name, password1, password2)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})