# Generated by Django 3.0 on 2021-09-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0014_auto_20210924_1035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='cartoon',
        ),
        migrations.AlterField(
            model_name='picture',
            name='type_picture',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Film'), (1, 'Serial'), (2, 'Cartoon'), (3, 'Anime'), (4, 'animated-series')], null=True),
        ),
    ]