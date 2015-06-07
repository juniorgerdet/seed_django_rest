#title           :pyscript.py
#description     :Extend letucce for implemented BDD on Django.
#author          :juniorgerdet
#date            :04-06-2015
#version         :0.4
#usage           :python manager harvest
#notes           :
#python_version  :2.7.10  
#==============================================================================
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Ride, Driver


# Create your views here.
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('role_alt',  'phone')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'profile')
        write_only_fields = ('password', )
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        if profile_data['role_alt']!="client":
            Driver.objects.create(user=user)
        return user
    def validate(self, attrs):
        invalid_email = True if User.objects.filter(email = attrs['email']) else False
        invalid_username = True if User.objects.filter(username = attrs['username']) else False
        if invalid_email:
            raise serializers.ValidationError("email_not_available")
        if invalid_username:
            raise serializers.ValidationError("username_not_available")
        return attrs
    

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('id', 'taxi_drive', 'client', 'destiny', 'active')


# return Response({
#                     'status': 'Unauthorized',
#                     'message': 'This account has been disabled.'
#                 }, status=status.HTTP_401_UNAUTHORIZED)

class DriverSerializer(serializers.ModelSerializer):
    rides = RideSerializer(many=True,read_only=True)
    class Meta:
        model = Driver
        fields = ('id', 'username', 'email', 'rides')
