# Generated by Django 3.2.6 on 2021-09-24 08:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0027_alter_post_ispublished'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedback', '0004_suggestedtag'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SugeestedCategory',
            new_name='SuggestedCategory',
        ),
    ]