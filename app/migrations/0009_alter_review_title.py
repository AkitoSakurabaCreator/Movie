# Generated by Django 4.1.3 on 2023-10-27 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_review_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=30, verbose_name='タイトル'),
        ),
    ]
