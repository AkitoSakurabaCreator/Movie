# Generated by Django 4.1.3 on 2023-10-27 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_alter_customuser_nick_name_alter_customuser_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='year',
            field=models.DateTimeField(blank=True, default='2023-10-27', null=True, verbose_name='生年月日'),
        ),
    ]
