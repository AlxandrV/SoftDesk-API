from json import JSONEncoder
from pydoc import importfile
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers

from .permissions import IsAuthenticatedProject, IsAuthenticatedContributor
from .serializers import RegisterSerializer, ProjectListSerializer, ContributorListSerializer
from .models import Projects, Issues, Comments, Contributors

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProjectViewSet(ModelViewSet):

    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticatedProject]

    def get_queryset(self):
        project_contribute = Contributors.objects.filter(user=self.request.user)
        projects = Projects.objects.filter(id__in=(project.project.id for project in project_contribute))
        return projects
    
class ContributorViewSet(ModelViewSet):

    serializer_class = ContributorListSerializer
    permission_classes = [IsAuthenticatedContributor]

    def get_queryset(self):
        queryset = Contributors.objects.filter(project=self.kwargs['project_pk'])
        return queryset

    def create(self, request, **kwargs):
        user = User.objects.get(id=request.data['id'])
        project = Projects.objects.get(id=kwargs['project_pk'])
        contributor = self.serializer_class.create(self, {'user': user, 'project': project})
        return JsonResponse({'user': f'{contributor.user} contribute to the project'})

    def destroy(self, request, *args, **kwargs):
        if Contributors.objects.filter(user=kwargs['pk']).exists():
            contributor = Contributors.objects.get(user=kwargs['pk'])
            if contributor.role == 'AUTHOR':
                return JsonResponse({'unauthorized': 'It is not allowed to delete the author'})
            else:
                self.perform_destroy(contributor)
                return JsonResponse({'delete': f'{contributor.user} contributor to be deleted'})
        else:
            raise serializers.ValidationError({'user': 'This user does not contribute to the project'})
