# Generated by Django 4.0.2 on 2022-02-27 13:03

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_profile_thumbnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='photo',
            new_name='profile_picture',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='thumbnail',
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
    ]
