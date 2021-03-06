# Generated by Django 2.1.4 on 2019-01-04 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edcmgmt', '0004_environment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('datatypeid', models.CharField(max_length=255)),
                ('multivalued', models.BooleanField()),
                ('suggestable', models.BooleanField()),
                ('sortable', models.BooleanField()),
                ('searchable', models.BooleanField()),
                ('facetable', models.BooleanField()),
                ('analyzer', models.CharField(max_length=255)),
                ('attr_config', models.TextField()),
            ],
        ),
    ]
