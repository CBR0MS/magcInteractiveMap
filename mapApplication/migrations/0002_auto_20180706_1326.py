# Generated by Django 2.0.4 on 2018-07-06 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapApplication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='long_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
