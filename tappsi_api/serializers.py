# -*- coding: utf-8 -*-
from .models import UserProfiles
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ParseError
# from rest_framework.pagination import PaginationSerializer
from datetime import datetime


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfiles
        fields = ('user', 'role_alt', 'gender', 'birthdate',  'phone', 'profile_pic')

class UserSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer()
    # role_alt = serializers.SerializerMethodField()
    role_alt = serializers.Field(source='profile.role_alt')
    class Meta:
        model = User
        fields = ('id', 'password', 'username', 'email', 'last_name', 'first_name', 'role_alt', 'is_active', 'date_joined')
        write_only_fields = ('password','is_active', 'date_joined',)
    def validate(self, attrs):
        
        invalid_email = False
        invalid_username = False
        exist_email = True if User.objects.filter(email = attrs['email']) else False
        # invalid_email = True if check_email else False
        exist_username = True if User.objects.filter(username = attrs['username']) else False
        # invalid_username = True if check_username else False
        if exist_username:
            raise serializers.ValidationError("{username_not_available}")
        if exist_email:
            raise serializers.ValidationError("email_not_available")
        return attrs
    # def get_role_alt(self, obj):
    #     up = UserProfiles.objects.get(user = obj.id)
    #     print up
    #     ser = UserProfileSerializer(up)
    #     return ser.data.role_alt

