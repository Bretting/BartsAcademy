# Generated by Django 4.2 on 2023-05-02 11:59

import Academy.models
from django.db import migrations, models
import django_resized.forms
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0002_category_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('blog_teaser', tinymce.models.HTMLField()),
                ('blog_image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, scale=None, size=[1000, 600], upload_to=Academy.models.image_upload_handler)),
                ('blog_text', tinymce.models.HTMLField()),
                ('blog_video', models.FileField(blank=True, null=True, upload_to='videos')),
                ('blog_footer_image', django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=75, scale=None, size=[1000, 600], upload_to=Academy.models.image_upload_handler)),
                ('blog_date_create', models.DateField(auto_now_add=True, null=True)),
                ('blog_date_edit', models.DateField(auto_now=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
    ]
