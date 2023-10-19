from django.core.management.base import BaseCommand
import pandas as pd
from GeromaApp.models import MotorVehicleValueGuide  # Import your app's model

# To run command, run code below
# python manage.py import_MV_guide_excel_data "D:\LARD GITHUB\GEROMA\UsedMVDatabase1stSeptember2023.xlsx"

class Command(BaseCommand):
    help = 'Import data from an Excel file into the SQLite database'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file to import')

    def handle(self, *args, **kwargs):
        excel_file_path = kwargs['excel_file']

        # Read data from Excel file
        try:
            df = pd.read_excel(excel_file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading Excel file: {e}'))
            return

        # Loop through the DataFrame and insert data into the database
        for _, row in df.iterrows():
            try:
                MotorVehicleValueGuide.objects.create(
                    HSCode=row['HSCode'],
                    CountryOfOrigin=row['COO'],
                    Description=row['Description'],
                    YearOfManufacture=row['YOM'],
                    Engine=row['CC'],
                    CIF=row['CIF'],
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error inserting data into database: {e}'))

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
