from rest_framework import permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj=None):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, User): 
            return obj.id == request.user.id        
        else:
            return False