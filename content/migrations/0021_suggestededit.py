# Generated by Django 3.2.6 on 2021-09-18 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0020_auto_20210918_1105'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuggestedEdit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('S', 'Suggested'), ('A', 'Rejected'), ('R', 'Acceptd')], max_length=1)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.post')),
            ],
        ),
    ]