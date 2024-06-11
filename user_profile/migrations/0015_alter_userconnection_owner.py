# Generated by Django 4.0.7 on 2022-09-20 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0014_rename_user_userconnection_connections'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconnection',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='connection', to='user_profile.userprofile'),
        ),
    ]
