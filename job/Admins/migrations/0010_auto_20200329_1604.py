# Generated by Django 2.2.1 on 2020-03-29 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admins', '0009_auto_20200324_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='check',
            old_name='job_name',
            new_name='j_name',
        ),
    ]