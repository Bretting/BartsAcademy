# Generated by Django 4.2 on 2024-05-04 09:19

import Academy.models
from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0043_rename_footer_image_blog_hero_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='hero_image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=100, scale=None, size=[1000, 600], upload_to=Academy.models.image_upload_handler),
        ),
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]