# Generated by Django 2.1.4 on 2019-01-05 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edcmgmt', '0006_attributes_attr_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributes',
            name='attr_orig_env',
            field=models.CharField(default='-', max_length=50),
        ),
    ]