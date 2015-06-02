from rest_framework import permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.timezone import now


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj=None):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, InformationPoint):
            return obj.owner == request.user
        elif isinstance(obj, Tag):
            return (True if obj.owner == request.user else self.IsAuthorized(request.method, request.user, obj, 1))
        elif isinstance(obj, Post):
            if request.method == 'DELETE':
                return True if request.user == obj.owner and obj.tag.write == True else False
            else:
                return True if obj.owner == request.user else self.IsAuthorized(request.method, request.user, obj, 2)
        elif isinstance(obj, User): 
            return obj.id == request.user.id        
        else:
            return False