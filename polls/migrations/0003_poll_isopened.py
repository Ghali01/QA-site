# Generated by Django 3.2.6 on 2021-10-05 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_pollitem_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='isOpened',
            field=models.BooleanField(default=False),
        ),
    ]
