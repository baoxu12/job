# Generated by Django 2.2.1 on 2020-04-06 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Boss', '0020_remove_job_job_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='C_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64, verbose_name='企业性质')),
            ],
            options={
                'db_table': 'c_type',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='c_staff',
            field=models.IntegerField(blank=True, choices=[(0, '少于10人'), (1, '10-49人'), (2, '50-99人'), (3, '100-499人'), (4, '500-999人'), (5, '1000-9999人'), (6, '10000人以上')], null=True, verbose_name='职员人数'),
        ),
        migrations.AddField(
            model_name='company',
            name='c_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Boss.C_type'),
        ),
    ]
