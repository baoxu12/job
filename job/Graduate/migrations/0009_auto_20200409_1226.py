# Generated by Django 2.2.1 on 2020-04-09 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Graduate', '0008_auto_20200329_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Boss.Job_table'),
        ),
    ]
