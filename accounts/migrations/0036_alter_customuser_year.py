# Generated by Django 4.1.3 on 2023-10-30 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_alter_customuser_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='year',
            field=models.DateTimeField(blank=True, default='2023-10-30', null=True, verbose_name='生年月日'),
        ),
    ]
