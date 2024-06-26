# Generated by Django 4.2 on 2023-06-22 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0032_alter_blog_bottle_tag_alter_blog_brand_tag_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='bottle_tag',
            field=models.ManyToManyField(blank=True, to='Academy.bottle'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='brand_tag',
            field=models.ManyToManyField(blank=True, to='Academy.brand'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='category_tag',
            field=models.ManyToManyField(blank=True, to='Academy.category'),
        ),
    ]
