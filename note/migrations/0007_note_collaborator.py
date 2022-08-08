# Generated by Django 4.0.5 on 2022-08-06 05:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('note', '0006_remove_note_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='collaborator',
            field=models.ManyToManyField(related_name='collaborator', to=settings.AUTH_USER_MODEL),
        ),
    ]
