# Generated by Django 4.2 on 2023-05-02 09:35

import Academy.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=Academy.models.video_upload_handler),
        ),
    ]
