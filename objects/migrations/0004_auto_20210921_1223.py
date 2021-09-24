# Generated by Django 3.0 on 2021-09-21 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0003_auto_20210919_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compilation',
            name='pictures',
        ),
        migrations.AddField(
            model_name='genre',
            name='slug',
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
    ]