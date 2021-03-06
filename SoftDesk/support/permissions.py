from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.permissions import BasePermission

from .models import Comments, Contributors, Issues

SAFE_METHODS = ['GET']

class IsAuthenticatedProject(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user
            and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            contributors = Contributors.objects.filter(project=obj).values('user')
            users = User.objects.filter(id__in=contributors)
            return bool(request.user in users)
        else:
            author = Contributors.objects.get(Q(project=obj) & Q(role='AUTHOR'))
            return bool(request.user == author.user)

class IsAuthenticatedContributor(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            contributors = Contributors.objects.filter(project=view.kwargs['project_pk']).values('user')
            users = User.objects.filter(id__in=contributors)
            return bool(request.user in users
                and request.user.is_authenticated)
        else:
            author = Contributors.objects.get(Q(project=view.kwargs['project_pk']) & Q(role='AUTHOR'))
            return bool(request.user == author.user
                and request.user.is_authenticated)

class IsAuthenticatedIssue(BasePermission):

    def has_permission(self, request, view):
        contributors = Contributors.objects.filter(project=view.kwargs['project_pk']).values('user')
        users = User.objects.filter(id__in=contributors)
        return bool(request.user in users
            and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.method == 'POST':
            contributors = Contributors.objects.filter(project=view.kwargs['project_pk']).values('user')
            users = User.objects.filter(id__in=contributors)
            return bool(request.user in users
                and request.user.is_authenticated)
        else:
            issue = Issues.objects.get(id=view.kwargs['pk'])
            return bool(request.user == issue.author_user
                and request.user.is_authenticated)

class IsAuthenticatedComment(BasePermission):

    def has_permission(self, request, view):
        contributors = Contributors.objects.filter(project=view.kwargs['project_pk']).values('user')
        users = User.objects.filter(id__in=contributors)
        return bool(request.user in users
            and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.method == 'POST':
            contributors = Contributors.objects.filter(project=view.kwargs['project_pk']).values('user')
            users = User.objects.filter(id__in=contributors)
            return bool(request.user in users
                and request.user.is_authenticated)
        else:
            comment = Comments.objects.get(id=view.kwargs['pk'])
            return bool(request.user == comment.author_user
                and request.user.is_authenticated)
