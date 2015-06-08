#title           :serializers.py
#description     :
#author          :juniorgerdet
#date            :04-06-2015
#version         :0.1
#usage           :
#notes           :
#python_version  :2.7.10  
#==============================================================================
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Ride, Driver
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
    
class ResumeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class RideSerializer(serializers.ModelSerializer):
    user_client=serializers.SerializerMethodField()
    user_driver=serializers.SerializerMethodField()
    class Meta:
        model = Ride
        fields = ("id", 'origin', 'destiny', 'taxi_driver', "client", 'user_client', 'user_driver', 'active')
        extra_kwargs = {'taxi_driver': {'write_only': True}, 'client': {'write_only': True}}
    def validate(self, attrs):
        if self.context["request"].method=='POST':
            ride_active = True if Ride.objects.filter(taxi_driver = self.context["request"].user, active=True) else False
            if ride_active:
                raise serializers.ValidationError("taxi_not_available")
        return attrs
    def update(self, instance, validated_data):
        instance.origin = validated_data.get('origin', instance.origin)
        instance.destiny = validated_data.get('destiny', instance.destiny)
        instance.client = validated_data.get('client', instance.client)
        instance.active = validated_data.get('active', instance.active)
        if not instance.active:
            Driver.objects.filter(user=self.context["request"].user).update(busy=False)
        instance.save()
        return instance
    def get_user_client(self, obj):
        return {'id': obj.client.id, 'first_name': obj.client.first_name , 'last_name' : obj.client.last_name}
    def get_user_driver(self, obj):
        return {'id': obj.taxi_driver.id, 'first_name': obj.taxi_driver.first_name, 'last_name' : obj.taxi_driver.last_name}


class DriverSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user.id',  read_only=True)
    first_name = serializers.ReadOnlyField(source='user.first_name',  read_only=True)
    last_name = serializers.ReadOnlyField(source='user.last_name',  read_only=True)
    username = serializers.ReadOnlyField(source='user.username',  read_only=True)
    email = serializers.ReadOnlyField(source='user.email',  read_only=True)
    class Meta:
        model = Driver
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'license_plate', 'busy')
