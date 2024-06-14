# Generated by Django 4.2 on 2024-06-14 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0053_bottle_bottle_date_create_bottle_bottle_date_edit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottle',
            name='image',
            field=models.URLField(help_text='Login to https://bartsbottles.nl/cp to search for the right image', max_length=255, verbose_name="Bart's Bottles image database url"),
        ),
    ]
