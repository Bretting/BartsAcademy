# Generated by Django 4.2 on 2023-06-14 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0025_category_tagline'),
    ]

    operations = [
        migrations.AddField(
            model_name='bottle',
            name='thumbnail',
            field=models.ImageField(default='1', upload_to=''),
            preserve_default=False,
        ),
    ]
