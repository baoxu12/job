# Generated by Django 2.2.1 on 2020-03-20 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Boss', '0008_auto_20200320_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='education',
            field=models.IntegerField(choices=[(0, '大专'), (1, '本科'), (2, '硕士'), (3, '博士')], verbose_name='学历'),
        ),
    ]
