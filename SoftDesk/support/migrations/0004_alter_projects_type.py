# Generated by Django 4.0.5 on 2022-06-20 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='type',
            field=models.IntegerField(choices=[(1, 'IOS'), (2, 'Android'), (3, 'Backend'), (4, 'Frontend')]),
        ),
    ]
