# Generated by Django 3.2.6 on 2021-09-23 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0026_alter_category_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='isPublished',
            field=models.BooleanField(default=True),
        ),
    ]
