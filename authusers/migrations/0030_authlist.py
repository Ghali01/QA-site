# Generated by Django 3.2.6 on 2021-10-14 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authusers', '0029_tmplink'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(choices=[('R', 'Register'), ('L', 'Login')], max_length=1)),
                ('title', models.TextField()),
                ('list', models.JSONField()),
            ],
        ),
    ]
