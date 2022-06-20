from pydoc import importfile
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, ProjectListSerializer
from .models import Projects, Issues, Comments

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProjectViewset(ModelViewSet):

    serializer_class = ProjectListSerializer
    queryset = Projects.objects.all()
    permission_classes = [IsAuthenticated]
