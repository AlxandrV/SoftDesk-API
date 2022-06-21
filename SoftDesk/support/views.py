from pydoc import importfile
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, ProjectListSerializer
from .models import Projects, Issues, Comments, Contributors

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProjectViewset(ModelViewSet):

    serializer_class = ProjectListSerializer
    queryset = Projects.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        project = Projects.objects.get(id=pk)
        author = Contributors.objects.filter(Q(project=project) & Q(role='AUTH'))[0]
        if author.user != request.user:
            return JsonResponse({"Permission": "You're not allowed to delete this project."})
        return super().destroy(request, pk)