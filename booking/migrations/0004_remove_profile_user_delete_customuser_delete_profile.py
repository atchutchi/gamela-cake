# Generated by Django 4.2.7 on 2023-11-22 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_customuser_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
