# Generated by Django 3.2.6 on 2021-10-15 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0004_alter_advertiseimage_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('ar', 'عربي'), ('en', 'English')], max_length=2)),
                ('page', models.TextField(default='')),
            ],
        ),
    ]