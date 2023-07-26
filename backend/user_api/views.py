from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		# print(data)
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		# username = UserSerializer()
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			# username = UserSerializer(serializer)
			# print(serializer.data)
			login(request, user)
			response_data = {
                'user': UserSerializer(user).data,  # Use your UserSerializer to customize the data sent to frontend
            }
			print(response_data)
			# print(request.session.keys())
			return Response(response_data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)

# @csrf_protect
class UserView(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		# print(request, 'request')
		serializer = UserSerializer(request.user)

		print(serializer.data, 'data')
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)
		# return Response(serializer.data, status=status.HTTP_200_OK)