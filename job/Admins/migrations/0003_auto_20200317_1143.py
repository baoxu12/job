# Generated by Django 2.2.1 on 2020-03-17 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admins', '0002_admins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admins',
            name='job_status',
            field=models.IntegerField(blank=True, choices=[(0, '待审核'), (1, '审核中'), (2, '已发布'), (3, '审核未通过'), (4, '已删除')], null=True, verbose_name='订单状态'),
        ),
    ]
