# Generated by Django 2.2.1 on 2020-03-24 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Graduate', '0005_auto_20200320_2201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='city',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='education',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='expect_job',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='honor',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='project',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='salary',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='school_experience',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='self_introduction',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='skill',
        ),
        migrations.AddField(
            model_name='hunter',
            name='city',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='意向城市'),
        ),
        migrations.AddField(
            model_name='hunter',
            name='education',
            field=models.TextField(blank=True, null=True, verbose_name='教育经历'),
        ),
        migrations.AddField(
            model_name='hunter',
            name='expect_job',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='意向岗位'),
        ),
        migrations.AddField(
            model_name='hunter',
            name='honor',
            field=models.TextField(blank=True, null=True, verbose_name='荣誉证书'),
        ),
        migrations.AddField(
            model_name='hunter',
            name='project',
            field=models.TextField(blank=True, null=True, verbose_name='项目经历'),
        ),
        migrations.AddField(
            model_name='hunter',
            name='salary',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='期望薪资'),
        ),
        migrations.AddField(
            model_name='hunter',
            name='school_experience',
            field=models.TextField(blank=True, null=True, verbose_name='在校经历'),
        ),
        migrations.AddField(
            model_name='hunter',
            name='self_introduction',
            field=models.TextField(blank=True, null=True, verbose_name='自我介绍'),
        ),
        migrations.AddField(
            model_name='hunter',
            name='skill',
            field=models.TextField(blank=True, null=True, verbose_name='相关技能'),
        ),
    ]
