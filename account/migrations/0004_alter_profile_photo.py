# Generated by Django 4.0.2 on 2022-02-14 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default=' ', upload_to='users/%Y/%m/%d/'),
        ),
    ]