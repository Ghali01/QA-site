# Generated by Django 3.2.6 on 2021-09-25 14:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0027_alter_post_ispublished'),
        ('authusers', '0015_baneduser'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='favQuestions',
            field=models.ManyToManyField(to='content.Question'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]