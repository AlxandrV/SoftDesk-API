from django.db.models import Q
from rest_framework.permissions import BasePermission

from .models import Contributors

class IsAuthorAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user
            and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        author = Contributors.objects.filter(Q(project=obj) & Q(role='AUTH'))[0]
        return bool(request.user == author.user)