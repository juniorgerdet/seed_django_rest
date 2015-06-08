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
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from user_agents import parse
from django.utils.encoding import smart_unicode
from rest_framework import renderers
from rest_framework.utils.urls import replace_query_param
from rest_framework_yaml.parsers import YAMLParser
from rest_framework_yaml.renderers import YAMLRenderer
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

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
    def create(self, request):  
        try:
            serializer=RideSerializer(data={'taxi_driver':request.user.id, 'client':request.DATA["client"], 'origin':request.DATA["origin"], 'destiny':request.DATA["destiny"]}, context= {'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception, e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

class AvailableView(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = (IsOwnerOrReadOnly,permissions.IsAuthenticated,)
    def initial(self, request, **kwargs):
        if request.user_agent.is_pc:
            self.renderer_classes = (TemplateHTMLRenderer,)
        elif request.user_agent.is_tablet:
            self.parser_classes=(YAMLParser,)
            self.renderer_classes = (YAMLRenderer,)
        elif request.user_agent.is_mobile:
            self.parser_classes=(JSONParser,)
            self.renderer_classes = (JSONRenderer,)
        else:
            self.parser_classes=(XMLParser,)
            self.renderer_classes = (XMLRenderer,)
    def get(self, request, **kwargs):
        try:
            drivers=Driver.objects.filter(busy=0)
            if request.user_agent.is_pc:
                serializer = DriverSerializer(drivers, many=True)
                return Response({'data':serializer.data}, template_name='index.html')
            else:
                paginator = CustomCoursePaginator()
                result_page = paginator.paginate_queryset(drivers, request)
                serializer = DriverSerializer(drivers, many=True)
                return paginator.get_paginated_response(serializer.data)
        except Exception, e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
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
        


class CustomCoursePaginator(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({'count': self.page.paginator.count,
                         'next': self.get_next_link(),
                         'previous': self.get_previous_link(),
                         'courses': data})

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return replace_query_param('', self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return replace_query_param('', self.page_query_param, page_number)