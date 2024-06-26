# Generated by Django 4.2 on 2024-05-17 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0052_auto_20240517_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='bottle',
            name='bottle_date_create',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='bottle',
            name='bottle_date_edit',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='brand_date_create',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='brand_date_edit',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='category_date_create',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='category_date_edit',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
