# Generated by Django 4.0.5 on 2022-06-20 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0004_alter_projects_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='type',
            field=models.CharField(choices=[('IOS', 'Ios'), ('ANDROID', 'Android'), ('BACKEND', 'Back End'), ('FRONTEND', 'Front End')], max_length=8),
        ),
    ]
