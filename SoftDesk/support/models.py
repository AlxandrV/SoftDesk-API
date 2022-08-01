from tkinter import CASCADE
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class Projects(models.Model):

    TYPE = (
        ('IOS', 'IOS'),
        ('ANDROID', 'Android'),
        ('BACKEND', 'Backend'),
        ('FRONTEND', 'Frontend'),
    )

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(choices=TYPE, max_length=8)

class Contributors(models.Model):

    ROLE = (
        ('AUTHOR', 'Auteur'),
        ('CONTRIBUTOR', 'Contributeur')
    )

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE, max_length=11, default='CONTRIBUTOR')

class Issues(models.Model):

    TAG = (
        ('BUG', 'Bug'),
        ('UPGRADE', 'Amélioration'),
        ('TASK', 'Tâche')
    )
    class Priority(models.IntegerChoices):
        HIGH = 1, _('Élevée')
        MEAN = 2, _('Moyenne')
        LOW = 3, _('Faible')

    class Status(models.TextChoices):
        TO_DO = 'TODO', _('À faire')
        IN_PROGRESS = 'INPROGRESS', _('En cours')
        DONE = 'DONE', _('Terminé')

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    tag = models.CharField(choices=TAG, max_length=7)
    priority = models.IntegerField(choices=Priority.choices)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, max_length=10, default=Status.TO_DO)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    assigned_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned')
    created_time = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):

    description = models.CharField(max_length=2048)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_comment')
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)