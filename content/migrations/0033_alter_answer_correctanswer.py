# Generated by Django 3.2.6 on 2021-10-08 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0032_auto_20211008_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='correctAnswer',
            field=models.BooleanField(null=True),
        ),
    ]