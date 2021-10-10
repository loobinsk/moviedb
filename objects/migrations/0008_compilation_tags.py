# Generated by Django 3.0 on 2021-10-06 07:04

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('objects', '0007_picture_similar_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='compilation',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
