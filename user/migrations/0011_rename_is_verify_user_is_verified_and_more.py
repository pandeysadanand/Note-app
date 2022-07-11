# Generated by Django 4.0.5 on 2022-07-11 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_user_is_verify_alter_user_location_alter_user_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_verify',
            new_name='is_verified',
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(default=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(default=True),
        ),
    ]
