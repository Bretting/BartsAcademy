# Generated by Django 4.2 on 2023-06-02 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0023_alter_bottle_sorting_alter_bottle_tech_aging_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bottle',
            name='tech_botanicals',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Botanicals'),
        ),
    ]
