# Generated by Django 4.0.5 on 2022-07-25 06:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0004_note_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 25, 11, 54, 47, 865476)),
        ),
    ]