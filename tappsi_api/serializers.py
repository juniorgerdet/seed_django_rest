from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Ride


# Create your views here.
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('role_alt', )

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
        fields = ('id', 'taxi_drive', 'client','origin', 'destiny', 'active')
    


# class RideSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ride
#         fields = ('id', 'taxi_drive', 'client','origin', 'destiny', 'active')
    

