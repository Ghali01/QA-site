# Generated by Django 3.2.6 on 2021-09-28 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authusers', '0021_alter_badgesuser_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='lastActive',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
