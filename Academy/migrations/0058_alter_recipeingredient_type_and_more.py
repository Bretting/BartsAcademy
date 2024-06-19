# Generated by Django 4.2 on 2024-06-18 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0057_recipe_alter_category_options_recipeingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='type',
            field=models.IntegerField(choices=[(1, 'Ml'), (2, 'Piece'), (3, 'Gram')], verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='unrelated_product',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
