# Import necessary modules
from GeromaApp.models import MotorVehicleValueGuide  # Replace 'your_app' with the actual app name

# python manage.py update_cifvalue_to_decimals

# Get all instances of the mvguide model
all_mvguide_instances = MotorVehicleValueGuide.objects.all()

# Iterate through the instances and update the cif values
for instance in all_mvguide_instances:
    cif_value = instance.CIF

    # Remove commas and convert to float
    cif_value = cif_value.replace(',', '')
    
    try:
        cif_value = float(cif_value)
    except ValueError:
        print(f"Invalid value in cif column: {cif_value}")
        continue

    # Update the instance with the new cif value
    instance.CIF = cif_value
    instance.save()
