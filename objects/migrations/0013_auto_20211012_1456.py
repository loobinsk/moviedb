# Generated by Django 3.0 on 2021-10-12 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0012_auto_20211012_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='preview',
            field=models.ImageField(upload_to='previews/'),
        ),
    ]
