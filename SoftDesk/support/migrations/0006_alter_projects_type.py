# Generated by Django 4.0.5 on 2022-06-21 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0005_alter_projects_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='type',
            field=models.CharField(choices=[('IOS', 'IOS'), ('ANDROID', 'Android'), ('BACKEND', 'Backend'), ('FRONTEND', 'Frontend')], max_length=8),
        ),
    ]
