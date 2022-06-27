from pydoc import importfile
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAuthorAuthenticated
from .serializers import RegisterSerializer, ProjectListSerializer, UserListSerializer
from .models import Projects, Issues, Comments, Contributors

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProjectViewset(ModelViewSet):

    serializer_class = ProjectListSerializer
    queryset = Projects.objects.all()
    permission_classes = [IsAuthorAuthenticated]

    def get_queryset(self):
        project_contribute = Contributors.objects.filter(user=self.request.user)
        projects = (project.project for project in project_contribute)
        return projects
    