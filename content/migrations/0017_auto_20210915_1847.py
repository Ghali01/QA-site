# Generated by Django 3.2.6 on 2021-09-15 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0016_auto_20210914_1803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='date',
        ),
        migrations.AddField(
            model_name='post',
            name='ActiveDate',
            field=models.DateField(auto_now=True),
        ),
    ]
