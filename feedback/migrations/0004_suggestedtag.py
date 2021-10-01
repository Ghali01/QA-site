# Generated by Django 3.2.6 on 2021-09-24 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0027_alter_post_ispublished'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedback', '0003_alter_sugeestedcategory_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuggestedTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.category')),
                ('suggester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]