# Generated by Django 3.2.6 on 2021-09-25 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('html', models.TextField()),
                ('language', models.CharField(choices=[('AR', 'عربي'), ('EN', 'English')], max_length=2)),
            ],
        ),
    ]
