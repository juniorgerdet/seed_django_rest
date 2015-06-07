#title           :pyscript.py
#description     :Extend letucce for implemented BDD on Django.
#author          :juniorgerdet
#date            :04-06-2015
#version         :0.1
#usage           :python manager harvest
#notes           :
#python_version  :2.7.10  
#==============================================================================
from django.contrib.auth.models import User
from tappsi_api.models import Profile, Ride, Driver
from tappsi_api.serializers import UserSerializer, RideSerializer, DriverSerializer
from rest_framework import viewsets, mixins, permissions, renderers, status, generics
from rest_framework.views import APIView
from tappsi_api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.cache import cache
from user_agents import parse
from django.utils.encoding import smart_unicode
from rest_framework import renderers

class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    def create(self, request):	
        try:
            email = request.DATA["email"].lower()
            email_exist = User.objects.filter(email = email)
            if email_exist:
                if email_exist[0].is_active:
                    return Response({'errors', 'user_not_available'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                serializer = UserSerializer(data={'username': request.DATA["username"], 'is_active': True, 'email': email, 'password': make_password(request.DATA['password'], None, 'pbkdf2_sha256'), 'first_name' : request.DATA['first_name'], 'last_name' : request.DATA['last_name'], 'profile' : {"role_alt":request.DATA["username"], "phone": "" if not 'phone' in request.DATA else request.DATA["phone"]}}, context= {'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception, e:
            return Response({'error': "invalid_request", "details": e}, status=status.HTTP_400_BAD_REQUEST)
 
class RideViewSet(ProtectedResourceView, viewsets.ModelViewSet):
    serializer_class = RideSerializer
    queryset = Ride.objects.all()
    permission_classes = (IsOwnerOrReadOnly,permissions.IsAuthenticated,)

class AvailableView(generics.ListAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    paginate_by = 100
    permission_classes = (IsOwnerOrReadOnly,permissions.IsAuthenticated,)
    def get(self, request, **kwargs):
        user_ids=Profile.objects.filter(role_alt='taxi_driver').values_list('user_id', flat=True)
        users=User.objects.filter(user=user_id, many=True)
        if request.user_agent.is_pc:
            serializer = DriverSerializer(users, many=True)
            print serializer.data
            return Response(serializer.data)
        elif request.user_agent.is_mobile:
            return  Response({'device': 'movil'}, status=status.HTTP_200_OK)
        elif request.user_agent.is_tablet: 
            return  Response({'device': 'is_tablet'}, status=status.HTTP_200_OK)
        """
            All attributes of user_agent
        """
         #  request.user_agent.is_touch_capable 
         #  request.user_agent.is_bot 

         #  request.user_agent.browser
         #  request.user_agent.browser.family 
         #  request.user_agent.browser.version 
         #  request.user_agent.browser.version_string 

         #  request.user_agent.os 
         #  request.user_agent.os.family 
         #  request.user_agent.os.version 
         #  request.user_agent.os.version_string 
