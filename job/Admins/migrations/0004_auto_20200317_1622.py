# Generated by Django 2.2.1 on 2020-03-17 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admins', '0003_auto_20200317_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_status', models.IntegerField(blank=True, choices=[(0, '待审核'), (1, '审核中'), (2, '已发布'), (3, '审核未通过'), (4, '已删除')], null=True, verbose_name='审核状态')),
            ],
            options={
                'db_table': 'check',
            },
        ),
        migrations.RemoveField(
            model_name='admins',
            name='job_status',
        ),
    ]