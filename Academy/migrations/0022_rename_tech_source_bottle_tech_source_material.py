# Generated by Django 4.2 on 2023-05-22 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0021_rename_tech_agave_bottle_tech_aging_barrels_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bottle',
            old_name='tech_source',
            new_name='tech_source_material',
        ),
    ]
