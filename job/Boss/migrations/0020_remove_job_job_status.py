# Generated by Django 2.2.1 on 2020-04-05 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Boss', '0019_job_check_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='job_status',
        ),
    ]