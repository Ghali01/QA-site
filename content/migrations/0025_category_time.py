# Generated by Django 3.2.6 on 2021-09-22 18:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0024_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]