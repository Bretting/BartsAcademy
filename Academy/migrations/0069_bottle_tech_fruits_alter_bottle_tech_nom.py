# Generated by Django 4.2 on 2024-08-09 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0068_recipe_occasion_recipe_taste'),
    ]

    operations = [
        migrations.AddField(
            model_name='bottle',
            name='tech_fruits',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Fruits'),
        ),
        migrations.AlterField(
            model_name='bottle',
            name='tech_nom',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='NOM'),
        ),
    ]