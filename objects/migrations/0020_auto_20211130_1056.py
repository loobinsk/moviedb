# Generated by Django 3.0 on 2021-11-30 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0019_сollectionсategory_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='сollectionсategory',
            name='collections',
            field=models.ManyToManyField(blank=True, null=True, to='objects.Compilation'),
        ),
    ]