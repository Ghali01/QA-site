# Generated by Django 3.2.6 on 2021-09-12 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20210911_1458'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='suggestedquestion',
            options={'ordering': ['date']},
        ),
    ]
