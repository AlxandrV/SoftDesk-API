from pydoc import importfile
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .permissions import IsAuthorAuthenticated
from .serializers import RegisterSerializer, ProjectListSerializer, ContributorListSerializer
from .models import Projects, Issues, Comments, Contributors

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProjectViewSet(ModelViewSet):

    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthorAuthenticated]

    def get_queryset(self):
        project_contribute = Contributors.objects.filter(user=self.request.user)
        projects = Projects.objects.filter(id__in=(project.project.id for project in project_contribute))
        return projects
    
class ContributorViewSet(ModelViewSet):

    serializer_class = ContributorListSerializer

    def get_queryset(self):
        queryset = Contributors.objects.filter(project=self.kwargs['project_pk'])
        return queryset

    def create(self, request, **kwargs):
        user = User.objects.get(id=request.data['id'])
        project = Projects.objects.get(id=kwargs['project_pk'])
        return self.serializer_class.create(self, {'user': user, 'project': project})
