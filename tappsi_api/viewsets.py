from django.contrib.auth.models import User
# from .models import UserProfileSerializer, UnitSerializer, History
from .serializers import UserSerializer
from rest_framework import viewsets, mixins, permissions, renderers, status
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def create(self, request):	
		try:
			email = request.DATA["email"].lower()
			user_exist = User.objects.filter(email = email)
			if user_exist:
				if not user_exist[0].is_active:
					ouser  = User.objects.filter(id = user_exist[0].id).update(is_active = True, password = make_password(request.DATA['password'], None, 'pbkdf2_sha256'))
					return Response(UserSerializer(ouser, context= {'request': request}).data, status=status.HTTP_200_OK)
				return Response({'errors', 'email_not_available'}, status=status.HTTP_406_NOT_ACCEPTABLE)
			else:
				print request.DATA['role_alt']	
				serializer = UserSerializer(data={'username': email[30] if len(email) > 30 else email, 'is_active': True, 'email': email, 'password': make_password(request.DATA['password'], None, 'pbkdf2_sha256'), 'first_name' : request.DATA['first_name'], 'last_name' : request.DATA['last_name'], 'role_alt' : request.DATA['role_alt']}, context= {'request': request})
				if serializer.is_valid():
					serializer.save()
					# ouser = User(id = serializer.data['id'], username = email, email = email, first_name = serializer.data['first_name'], last_name = serializer.data['last_name']) 
					return Response(serializer.data, status=status.HTTP_201_CREATED)
				else:
					return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
		except Exception, e:
			print e
			return Response({'errors': "invalid_request"}, status=status.HTTP_400_BAD_REQUEST)
    