# Generated by Django 4.2 on 2024-08-11 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0071_blogvideo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogvideo',
            name='video_url',
        ),
        migrations.AddField(
            model_name='blogvideo',
            name='video',
            field=models.FileField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
