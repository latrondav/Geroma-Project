# Generated by Django 4.2.4 on 2023-09-19 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeromaApp', '0005_hscodes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hscodes',
            name='heading',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='hscodes',
            name='hs_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='hscodes',
            name='rate',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='hscodes',
            name='unit_of_quantity',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
