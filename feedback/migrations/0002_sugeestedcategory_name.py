# Generated by Django 3.2.6 on 2021-09-23 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sugeestedcategory',
            name='name',
            field=models.CharField(default='', max_length=60),
            preserve_default=False,
        ),
    ]
