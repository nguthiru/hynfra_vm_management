# Generated by Django 5.1.1 on 2024-09-08 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('standard', 'Standard User'), ('guest', 'Guest')], default='standard', max_length=20),
        ),
    ]
