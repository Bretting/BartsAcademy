# Generated by Django 4.2 on 2024-08-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0077_alter_bottle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottle',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]