# Generated by Django 3.2.6 on 2021-09-14 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_question_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postlog',
            options={},
        ),
        migrations.RemoveField(
            model_name='postlog',
            name='time',
        ),
    ]
