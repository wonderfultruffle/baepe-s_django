# Generated by Django 4.2.4 on 2023-08-19 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmark',
            name='url',
        ),
        migrations.AddField(
            model_name='bookmark',
            name='site_url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
