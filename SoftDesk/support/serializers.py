from dataclasses import field
from wsgiref.validate import validator
from django.forms import ChoiceField
from django.http import JsonResponse
from django.conf import settings

from pkg_resources import require
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from rest_framework.validators import UniqueValidator

from .models import Projects, Issues, Comments, Contributors

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProjectListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields = '__all__'

    def create(self, validated_data):
        project = Projects.objects.create(**validated_data)
        project.save()
        contributor = Contributors.objects.create(
            user=self.context['request'].user,
            project=project,
            role='AUTHOR'
        )
        contributor.save()
        return project

class ContributorListSerializer(serializers.ModelSerializer):

    class EmbeddedUserSerializer(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = ('username', 'id')

    user = EmbeddedUserSerializer()

    class Meta:
        model = Contributors
        exclude = ('project',)

    def create(self, validated_data):
        contributor = Contributors.objects.filter(Q(project=validated_data['project']) & Q(user=validated_data['user']) & Q(role='CONTRIBUTOR'))
        if not contributor :
            contributor = Contributors.objects.create(**validated_data)
            contributor.save()
            return contributor
        else:
            raise serializers.ValidationError({'user': 'This user is already contributing to this project'})


class IssueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issues
        fields = '__all__'
        extra_kwargs = {'author_user': {'read_only': True},'assigned_user': {'read_only': True}}


class CommentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'
