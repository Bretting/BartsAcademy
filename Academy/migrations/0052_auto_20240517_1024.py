# Generated by Django 4.2 on 2024-05-17 08:24

from django.db import migrations

def set_site_domain(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    site = Site.objects.get(id=1)
    site.domain = 'bartsacademy.nl'
    site.name = 'Barts Academy'
    site.save()

class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('Academy', '0051_alter_blog_hero_image_alter_blogimage_image_and_more'),
    ]

    operations = [
        migrations.RunPython(set_site_domain),
    ]
