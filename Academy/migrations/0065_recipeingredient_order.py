# Generated by Django 4.2 on 2024-06-21 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0064_recipe_recipe_steps_alter_recipeingredient_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredient',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]