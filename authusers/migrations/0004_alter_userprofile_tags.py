# Generated by Django 3.2.6 on 2021-09-01 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_tag'),
        ('authusers', '0003_auto_20210901_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='tags',
            field=models.ManyToManyField(to='content.Tag'),
        ),
    ]
