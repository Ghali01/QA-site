# Generated by Django 3.2.6 on 2021-10-08 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0034_alter_answer_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='content.post'),
        ),
    ]