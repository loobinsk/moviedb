# Generated by Django 3.0 on 2021-09-19 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0002_auto_20210919_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='compilation',
            name='poster',
            field=models.TextField(default=1, verbose_name='ссылка на постер подборки'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='frame',
            name='url',
            field=models.TextField(verbose_name='ссылка на кадр'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='poster',
            field=models.TextField(verbose_name='ссылка на постер'),
        ),
    ]
