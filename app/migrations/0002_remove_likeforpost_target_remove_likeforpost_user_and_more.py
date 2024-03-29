# Generated by Django 4.1.3 on 2023-10-05 05:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likeforpost',
            name='target',
        ),
        migrations.RemoveField(
            model_name='likeforpost',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='item',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'レビュー一覧', 'verbose_name_plural': 'レビュー一覧'},
        ),
        migrations.RemoveField(
            model_name='review',
            name='bought',
        ),
        migrations.RemoveField(
            model_name='review',
            name='content_id',
        ),
        migrations.AddField(
            model_name='review',
            name='movie_id',
            field=models.IntegerField(default=1, max_length=255, verbose_name='アイテムID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新日'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=255, verbose_name='タイトル'),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='LikeForPost',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
