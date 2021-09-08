# Generated by Django 3.2.6 on 2021-09-01 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pathlib


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_tag'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authusers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.CharField(max_length=70)),
                ('about', models.TextField()),
                ('image', models.ImageField(default='default.jpg', upload_to=pathlib.PureWindowsPath('E:/projects/interviewsquestion/back-end/media/profile'))),
                ('tags', models.ManyToManyField(to='content.Tag')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
