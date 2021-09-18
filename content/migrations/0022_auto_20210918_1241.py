# Generated by Django 3.2.6 on 2021-09-18 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0021_suggestededit'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlog',
            name='edit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='content.suggestededit'),
        ),
        migrations.AlterField(
            model_name='postlog',
            name='type',
            field=models.CharField(choices=[('S', 'Suggest'), ('A', 'Accept'), ('R', 'Reject'), ('SE', 'Suggest Edit'), ('AE', 'Accept Edit'), ('RE', 'Reject Edit'), ('P', 'Publish'), ('UP', 'Unpublish')], max_length=4),
        ),
    ]