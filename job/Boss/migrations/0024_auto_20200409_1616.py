# Generated by Django 2.2.1 on 2020-04-09 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Boss', '0023_auto_20200409_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_table',
            name='send_status',
            field=models.IntegerField(choices=[(0, '未查看'), (1, '已查看'), (2, '已发送邀请'), (3, '邀请面试成功'), (4, '不合适'), (5, '邀请面试失败'), (6, '面试通过'), (7, '面试未通过'), (8, '录用通知已发送')], verbose_name='投递状态'),
        ),
    ]
