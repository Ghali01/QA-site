# Generated by Django 3.2.6 on 2021-09-30 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authusers', '0023_alter_userprofile_lastactive'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='badgesuser',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='rep',
            field=models.IntegerField(default=0),
        ),
    ]
