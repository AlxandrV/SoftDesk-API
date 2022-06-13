from django.conf import settings
from django.db import models
from django import forms

class Projects(models.Model):

    class Type(models.IntegerChoices):
        IOS = 1
        ANDROID = 2
        BACK_END = 3
        FRONT_END = 4

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.IntegerField(choices=Type.choices)

class Contributors(models.Model):

    class Role(models.TextChoices):
        AUTHOR = 'AUTH'
        CONTRIBUTOR = 'CONT'

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    role = models.CharField(choices=Role.choices, max_length=4)