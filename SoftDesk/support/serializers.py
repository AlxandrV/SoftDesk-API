from dataclasses import field
from wsgiref.validate import validator
from django.forms import ChoiceField
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
    
    type = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = '__all__'

    def get_type(self, obj):
        return obj.get_type_display()

    def create(self, validated_data):
        project = Projects.objects.create(**validated_data)
        project.save()
        contributor = Contributors.objects.create(
            user=self.context['request'].user,
            project=project,
            role='AUTH'
        )
        contributor.save()
        return project

    def update(self, instance, validated_data):
        author = Contributors.objects.filter(Q(project=instance) & Q(role='AUTH'))[0]
        if author.user != self.context['request'].user:
            raise serializers.ValidationError({"Permission": "You're not allowed to update this project."})
        return super().update(instance, validated_data)
