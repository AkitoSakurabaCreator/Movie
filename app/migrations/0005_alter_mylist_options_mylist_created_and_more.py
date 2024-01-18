# Generated by Django 4.1.3 on 2023-10-06 09:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_review_backdrop_path_alter_review_poster_path'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mylist',
            options={'verbose_name': 'マイリスト一覧', 'verbose_name_plural': 'マイリスト一覧'},
        ),
        migrations.AddField(
            model_name='mylist',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日'),
        ),
        migrations.AlterField(
            model_name='review',
            name='movie_id',
            field=models.IntegerField(verbose_name='アイテムID'),
        ),
    ]
