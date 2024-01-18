# Generated by Django 4.1.3 on 2023-10-05 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_review_poster_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='backdrop_path',
            field=models.CharField(default=1, max_length=255, verbose_name='背景画像'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='poster_path',
            field=models.CharField(max_length=255, verbose_name='ポスター画像'),
        ),
    ]
