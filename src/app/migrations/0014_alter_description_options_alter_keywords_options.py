# Generated by Django 5.1.1 on 2024-12-26 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_description_description_keywords'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='description',
            options={'verbose_name': 'サイト詳細', 'verbose_name_plural': 'サイト詳細'},
        ),
        migrations.AlterModelOptions(
            name='keywords',
            options={'verbose_name': 'キーワード', 'verbose_name_plural': 'キーワード'},
        ),
    ]
