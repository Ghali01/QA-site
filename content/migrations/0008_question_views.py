# Generated by Django 3.2.6 on 2021-09-13 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_auto_20210913_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='views',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]