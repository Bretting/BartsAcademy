# Generated by Django 4.2 on 2024-08-26 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0078_alter_bottle_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottle',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
