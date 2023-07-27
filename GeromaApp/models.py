from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Contacts(models.Model):
    contact_name = models.CharField(max_length=100, null=False, blank=False)
    contact_email = models.EmailField(null=False, blank=False)
    contact_subject = models.CharField(max_length=100, null=False, blank=False)
    contact_message = models.TextField(max_length=100,)

    def __str__(self):
        return str(self.contact_name)

class Profile(models.Model):
    user =  models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    contact = models.CharField(max_length=100, null=False, blank=False)
    regno = models.CharField(max_length=100, null=False, blank=False)
    campus = models.CharField(max_length=100, null=False, blank=False)
    course = models.CharField(max_length=100, null=False, blank=False)
    yos = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return str(self.user)
    

class Events(models.Model):
    event_name = models.CharField(max_length=100, null=False, blank=False)
    event_image = models.ImageField(upload_to="events_images", null=False, blank=False)
    event_description = models.TextField(max_length=100,)

    def __str__(self):
        return str(self.event_name)

class Orders(models.Model):
    user_id = models.CharField(max_length = 100, null = False, blank = False)
    order_name = models.CharField(max_length = 100, null = False, blank = False)
    order_course = models.CharField(max_length = 100, null = False, blank = False)
    order_yos = models.CharField(max_length = 100, null = False, blank = False)
    order_email = models.EmailField(max_length = 100, null = False, blank = False)
    order_contact = models.CharField(max_length = 100, null = False, blank = False)
    order_exec_shirt = models.CharField(max_length = 100, null = False, blank = False)
    order_tshirt = models.CharField(max_length = 100, null = False, blank = False)
    order_sicaid = models.CharField(max_length = 100, null = False, blank = False)
    order_status = models.CharField(max_length = 100, null = False, blank = False)
    
    def __str__(self):
        return str(self.order_name)

class Alumni_Carbinets(models.Model):
    carbinet_name = models.CharField(max_length = 100, null = False, blank = False)
    carbinet_description = models.TextField(max_length=200)
    carbinet_image = models.ImageField(upload_to="alumni_carbinet_images", null=False, blank=False)
    president = models.CharField(max_length = 100, null = False, blank = False)
    vice_president = models.CharField(max_length = 100, null = False, blank = False)
    general_secretary = models.CharField(max_length = 100, null = False, blank = False)
    secretary = models.CharField(max_length = 100, null = False, blank = False)
    speaker = models.CharField(max_length = 100, null = False, blank = False)
    deputy_speaker = models.CharField(max_length = 100, null = False, blank = False)
    finance_manager = models.CharField(max_length = 100, null = False, blank = False)
    deputy_finance_manager = models.CharField(max_length = 100, null = False, blank = False)
    legal_advisor = models.CharField(max_length = 100, null = False, blank = False)
    chief_editor = models.CharField(max_length = 100, null = False, blank = False)
    deputy_chief_editor = models.CharField(max_length = 100, null = False, blank = False)
    public_relations_manager = models.CharField(max_length = 100, null = False, blank = False)
    deputy_public_relations_manager = models.CharField(max_length = 100, null = False, blank = False)
    organizing_secretary = models.CharField(max_length = 100, null = False, blank = False)
    deputy_organizing_secretary = models.CharField(max_length = 100, null = False, blank = False)
    project_manager = models.CharField(max_length = 100, null = False, blank = False)
    deputy_project_manager = models.CharField(max_length = 100, null = False, blank = False)
    events_manager = models.CharField(max_length = 100, null = False, blank = False)
    deputy_events_manager = models.CharField(max_length = 100, null = False, blank = False)
    mobiliser = models.CharField(max_length = 100, null = False, blank = False)
    deputy_mobiliser = models.CharField(max_length = 100, null = False, blank = False)
    inclusive_officer = models.CharField(max_length = 100, null = False, blank = False)

    def __str__(self):
        return str(self.carbinet_name)


