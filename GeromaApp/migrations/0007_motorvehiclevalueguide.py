# Generated by Django 4.2.4 on 2023-10-19 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeromaApp', '0006_alter_hscodes_heading_alter_hscodes_hs_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotorVehicleValueGuide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HSCode', models.CharField(max_length=255)),
                ('CountryOfOrigin', models.CharField(max_length=255)),
                ('Description', models.TextField()),
                ('YearOfManufacture', models.PositiveIntegerField()),
                ('Engine', models.PositiveIntegerField()),
                ('CIF', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
