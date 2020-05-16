# Generated by Django 3.0.6 on 2020-05-16 11:35

import apps.video.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to=apps.video.models.UploadTo('originals'))),
                ('preview', models.ImageField(blank=True, null=True, upload_to=apps.video.models.UploadTo('previews'))),
                ('mp4', models.FileField(blank=True, null=True, upload_to=apps.video.models.UploadTo('mp4'))),
                ('webm', models.FileField(blank=True, null=True, upload_to=apps.video.models.UploadTo('webm'))),
            ],
            options={
                'abstract': False,
            },
        ),
    ]