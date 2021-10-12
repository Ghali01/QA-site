# Generated by Django 3.2.6 on 2021-10-12 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0036_alter_answer_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postlog',
            name='type',
            field=models.CharField(choices=[('S', 'Suggest'), ('A', 'Accept'), ('R', 'Reject'), ('SE', 'Suggest Edit'), ('AE', 'Accept Edit'), ('RE', 'Reject Edit'), ('P', 'Publish'), ('UP', 'Ubpunlish')], max_length=4),
        ),
    ]
