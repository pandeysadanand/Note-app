# Generated by Django 4.0.5 on 2022-06-29 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='author_id',
            new_name='note_id',
        ),
    ]