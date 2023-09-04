from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication


# Create your views here.
class RegAPIView(APIView):
	def post(self, r):
		data = r.data
		if 'username' in data and 'password' in data and 'email' in data:
			user = User(username=data['username'], password=data['password'], email=data['email'])
			user.save()
			return Response({"detail": "Registration Successful."}, status=status.HTTP_200_OK)
		return Response({"detail": "Fields Missing."}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, r):
        username = r.data['username']
        password = r.data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(r, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        else:
            raise exceptions.AuthenticationFailed('No such user')

   
class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, r):
        user = r.user
        if user.is_authenticated:
            token = Token.objects.get(user=user)
            token.delete()
            # r.user.auth_token.delete()
            logout(r)
        return Response({"detail": "Logout Successful."}, status=status.HTTP_200_OK)