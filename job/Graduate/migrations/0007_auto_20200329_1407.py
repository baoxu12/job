# Generated by Django 2.2.1 on 2020-03-29 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Graduate', '0006_auto_20200324_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='hunter',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resume', verbose_name='简历'),
        ),
        migrations.DeleteModel(
            name='Resume',
        ),
    ]