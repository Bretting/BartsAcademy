# Generated by Django 4.2 on 2024-04-05 08:07

import Academy.models
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0040_alter_blog_footer_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogimage',
            name='name',
        ),
        migrations.AlterField(
            model_name='blogimage',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=100, scale=None, size=[1000, 600], upload_to=Academy.models.image_upload_handler),
        ),
    ]