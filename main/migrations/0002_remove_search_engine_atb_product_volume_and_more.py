# Generated by Django 4.1.7 on 2023-03-10 18:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='search_engine_atb',
            name='product_volume',
        ),
        migrations.AlterField(
            model_name='search_engine_arsen',
            name='search_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 10, 20, 39, 24, 914833)),
        ),
        migrations.AlterField(
            model_name='search_engine_atb',
            name='search_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 10, 20, 39, 24, 916014)),
        ),
        migrations.AlterField(
            model_name='search_engine_silpo',
            name='search_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 10, 20, 39, 24, 914833)),
        ),
    ]