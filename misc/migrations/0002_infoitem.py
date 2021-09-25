# Generated by Django 3.2.6 on 2021-09-24 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('language', models.CharField(choices=[('AR', 'عربي'), ('EN', 'English')], max_length=2)),
            ],
        ),
    ]
