# Generated by Django 2.2.1 on 2020-03-18 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Graduate', '0002_auto_20200318_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hunter',
            name='type',
            field=models.CharField(max_length=4, verbose_name='类别'),
        ),
    ]