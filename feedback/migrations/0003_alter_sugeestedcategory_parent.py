# Generated by Django 3.2.6 on 2021-09-24 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0027_alter_post_ispublished'),
        ('feedback', '0002_sugeestedcategory_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sugeestedcategory',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='content.category'),
        ),
    ]