# Generated by Django 3.2.6 on 2021-10-03 19:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0030_alter_badge_reason'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedback', '0008_rename_report_postreport_reporter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='content.post')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.flagreason')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportsM', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='PostReport',
        ),
    ]
