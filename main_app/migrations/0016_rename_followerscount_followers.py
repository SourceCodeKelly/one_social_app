# Generated by Django 4.0.5 on 2022-06-09 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_followerscount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FollowersCount',
            new_name='Followers',
        ),
    ]