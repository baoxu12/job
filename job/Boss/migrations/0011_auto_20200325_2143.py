# Generated by Django 2.2.1 on 2020-03-25 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Boss', '0010_auto_20200325_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boss',
            name='work_status',
            field=models.IntegerField(blank=True, choices=[(0, '在职'), (1, '离职'), (2, '停职')], null=True, verbose_name='在职信息'),
        ),
    ]
