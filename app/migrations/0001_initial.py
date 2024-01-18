# Generated by Django 4.1.3 on 2023-10-04 03:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='タイトル')),
                ('price', models.IntegerField(verbose_name='値段')),
                ('category', models.CharField(max_length=100, verbose_name='カテゴリー')),
                ('brand', models.CharField(max_length=100, verbose_name='ブランド')),
                ('slug', models.SlugField(verbose_name='固有ID')),
                ('description', models.TextField(verbose_name='商品説明')),
                ('sex', models.CharField(choices=[('自由', '自由'), ('男性', '男性'), ('女性', '女性')], default='自由', max_length=5, verbose_name='性別')),
                ('color', models.CharField(choices=[('白', '白'), ('グレー', 'グレー'), ('黒', '黒'), ('ピンク', 'ピンク'), ('赤', '赤'), ('オレンジ', 'オレンジ'), ('ベージュ', 'ベージュ'), ('茶', '茶'), ('黄', '黄'), ('緑', '緑'), ('青', '青'), ('紫', '紫'), ('ネイビー', 'ネイビー'), ('カーキ', 'カーキ'), ('ゴールド', 'ゴールド'), ('アザー', 'アザー'), ('アイボリー', 'アイボリー'), ('オリーブ', 'オリーブ')], default='None', max_length=10, verbose_name='色')),
                ('image', models.ImageField(upload_to='products_images', verbose_name='イメージ画像')),
                ('upload_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='担当者')),
            ],
            options={
                'verbose_name': '商品一覧',
                'verbose_name_plural': '商品一覧',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_id', models.SlugField(verbose_name='アイテムID')),
                ('title', models.CharField(max_length=200, verbose_name='タイトル')),
                ('content', models.TextField(verbose_name='本文')),
                ('like', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='評価')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('bought', models.BooleanField(default=False, verbose_name='購入者')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '商品レビュー一覧',
                'verbose_name_plural': '商品レビュー一覧',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('ordered_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '注文一覧',
                'verbose_name_plural': '注文一覧',
            },
        ),
        migrations.CreateModel(
            name='MyList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikeForPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
