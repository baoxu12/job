# Generated by Django 2.2.1 on 2020-03-18 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Boss', '0003_auto_20200317_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boss',
            name='b_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Boss.Company'),
        ),
        migrations.AlterField(
            model_name='boss',
            name='b_resume',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Boss.Hr_job'),
        ),
    ]
