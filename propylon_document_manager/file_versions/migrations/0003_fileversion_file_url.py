# Generated by Django 4.1.9 on 2023-07-27 18:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("file_versions", "0002_fileversion_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="fileversion",
            name="file_url",
            field=models.URLField(default=""),
            preserve_default=False,
        ),
    ]
