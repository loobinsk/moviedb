# Generated by Django 3.0 on 2021-10-03 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0005_auto_20211003_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compilation',
            name='main_genre',
            field=models.ManyToManyField(related_name='collections_genre', to='objects.Genre'),
        ),
        migrations.AlterField(
            model_name='compilation',
            name='pictures',
            field=models.ManyToManyField(related_name='collections', to='objects.Picture'),
        ),
        migrations.DeleteModel(
            name='SimilarPictures',
        ),
    ]
