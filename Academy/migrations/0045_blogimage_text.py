# Generated by Django 4.2 on 2024-05-05 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0044_alter_blog_hero_image_alter_blog_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogimage',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
