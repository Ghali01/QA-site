# Generated by Django 3.2.6 on 2021-09-23 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('authusers', '0014_alter_userprofile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='BanedUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
            ],
        ),
    ]
