# Generated by Django 2.1.4 on 2019-01-17 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edcmgmt', '0008_auto_20190117_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='edc_version',
            field=models.CharField(choices=[('10.1.0', '10.1'), ('10.1.1', '10.1.1'), ('10.2.0', '10.2'), ('10.2.1', '10.2.1'), ('10.2.2', '10.2.2')], max_length=15),
        ),
    ]
