# Generated by Django 4.2 on 2024-08-26 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0076_recipeoccasion_recipetaste_recipetype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottle',
            name='name',
            field=models.TextField(),
        ),
    ]