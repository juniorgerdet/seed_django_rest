
from django.contrib.auth.models import User
from .models import Profile, Ride
from .serializers import UserSerializer, RideSerializer
from rest_framework import viewsets, mixins, permissions, renderers, status, generics
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
from django.db.models import Q

class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
	serializer_class = UserSerializer
	queryset = User.objects.all()
	permission_classes = (IsOwnerOrReadOnly,)
	def create(self, request):	
		try:
			email = request.DATA["email"].lower()
			profile={"role_alt":request.DATA['role_alt']}
			user_exist = User.objects.filter(email = email)
			if user_exist:
				if user_exist[0].is_active:
					return Response({'errors', 'user_not_available'}, status=status.HTTP_406_NOT_ACCEPTABLE)
			else:	
				serializer = UserSerializer(data={'username': request.DATA["username"], 'is_active': True, 'email': email, 'password': make_password(request.DATA['password'], None, 'pbkdf2_sha256'), 'first_name' : request.DATA['first_name'], 'last_name' : request.DATA['last_name'], 'profile' : profile}, context= {'request': request})
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
	def perform_create(self, serializer):
            serializer.save(taxi_drive=self.request.user)

class ContactViewSet(generics.ListAPIView):
	def list(self, request):
		# queryset = User.objects.all()
  		#serializer = UserSerializer(queryset, many=True)
  		#return Response(serializer.data)
		# table1.objects.exclude(id__in=table2.objects.filter(your_condition).values_list('id', flat=True))  		
		# users = User.objects.filter(pk__in=taxis_availables)
		# table1.objects.exclude(id__in=table2.objects.filter(your_condition).values_list('id', flat=True))  		
		user=User.objects.filter(role_alt="taxi_drive").values_list('id', flat=True)
		rides = Ride.objects.filter(active=0)
		try:
			page = paginator.page(request.QUERY_PARAMS.get('page'))
		except Exception, e:
			page = paginator.page(1)
		serializer = PaginatedUserContactSerializer(page, context={'user' : request.user.id})
		return Response(serializer.data, status=status.HTTP_200_OK)

class UserContactSerializer(serializers.ModelSerializer):
    username = serializers.Field(source='contact.username')
    email = serializers.Field(source='contact.email')
    class Meta:
        model = UserContact
        fields = ('id', 'contact', 'user', 'username', 'email')
        write_only_fields=('user',)

    def validate(self, attrs):
        check_contact = UserContact.objects.filter(contact = attrs['contact'], user = attrs['user'])
        if check_contact:
            raise serializers.ValidationError("contact_exist")
        return attrs 