from tkinter import CASCADE
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

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

class Issues(models.Model):

    class Tag(models.TextChoices):
        BUG = 'BUG', _('Bug')
        UPGRADE = 'UGD', _('Amélioration')
        TASK = 'TASK', _('Tâche')

    class Priority(models.IntegerChoices):
        HIGH = 1, _('Élevée')
        MEAN = 2, _('Moyenne')
        LOW = 3, _('Faible')

    class Status(models.TextChoices):
        TO_DO = 'TD', _('À faire')
        IN_PROGRESS = 'IP', _('En cours')
        DONE = 'DN', _('Terminé')

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    tag = models.CharField(choices=Tag.choices, max_length=4)
    priority = models.IntegerField(choices=Priority.choices)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, max_length=2)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    assigned_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned')
    created_time = models.DateTimeField(auto_now_add=True)