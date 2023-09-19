from django.core.management.base import BaseCommand
from GeromaApp.models import HSCodes  # Import your app's model
from django.db import connection

# To run Command
# python manage.py replace_nan_with_blank


class Command(BaseCommand):
    help = 'Replace "nan" values with empty strings in all string fields of the database'

    def handle(self, *args, **kwargs):
        try:
            model_fields = HSCodes._meta.get_fields()
            update_fields = []

            with connection.cursor() as cursor:
                for field in model_fields:
                    if field.is_relation:
                        continue  # Skip fields that are relationships (foreign keys, etc.)

                    if not field.get_internal_type() == 'CharField':
                        continue  # Skip fields that are not string fields

                    field_name = field.get_attname_column()[0]
                    query = f"UPDATE {HSCodes._meta.db_table} SET {field_name} = '' WHERE {field_name} = 'nan';"
                    cursor.execute(query)
                    update_fields.append(field_name)

            if update_fields:
                self.stdout.write(self.style.SUCCESS(f'Successfully replaced "nan" values with empty strings in string fields: {", ".join(update_fields)}'))
            else:
                self.stdout.write(self.style.SUCCESS('No string fields were updated.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
