# Generated by Django 4.0.2 on 2022-02-28 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=225, unique_for_date='published_date'),
        ),
    ]
