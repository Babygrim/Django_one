# Generated by Django 4.1.7 on 2023-03-20 11:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='search_engine_atb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_request', models.CharField(max_length=200)),
                ('product_name', models.CharField(max_length=200)),
                ('product_price', models.CharField(max_length=200)),
                ('search_date', models.DateTimeField(default=datetime.date(2023, 3, 20))),
                ('product_image', models.CharField(max_length=300)),
            ],
            options={
                'ordering': ['-search_date'],
            },
        ),
        migrations.CreateModel(
            name='search_engine_glove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_request', models.CharField(max_length=200)),
                ('product_name', models.CharField(max_length=200)),
                ('product_price', models.CharField(max_length=200)),
                ('product_volume', models.CharField(max_length=200)),
                ('search_date', models.DateTimeField(default=datetime.date(2023, 3, 20))),
                ('product_image', models.CharField(max_length=300)),
            ],
            options={
                'ordering': ['-search_date'],
            },
        ),
        migrations.CreateModel(
            name='search_engine_silpo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_request', models.CharField(max_length=200)),
                ('product_name', models.CharField(max_length=200)),
                ('product_price', models.CharField(max_length=200)),
                ('product_volume', models.CharField(max_length=200)),
                ('search_date', models.DateTimeField(default=datetime.date(2023, 3, 20))),
                ('product_image', models.CharField(max_length=300)),
            ],
            options={
                'ordering': ['-search_date'],
            },
        ),
    ]
