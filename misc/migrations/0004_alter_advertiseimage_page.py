# Generated by Django 3.2.6 on 2021-09-25 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0003_contactmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertiseimage',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='misc.advertisepage'),
        ),
    ]