# Generated by Django 2.2.1 on 2020-03-24 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admins', '0008_auto_20200318_1643'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admins',
            old_name='phone_number',
            new_name='phone',
        ),
    ]