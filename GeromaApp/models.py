from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

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

class TaxCalculation(models.Model):
    cif = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)  # Assuming currency code like USD, EUR, UGX
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust digits as needed
    hscode = models.CharField(max_length=10) 
    hscode_description = models.TextField()
    unit_of_measure = models.CharField(max_length=10, blank=True, null=True)
    measurement = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='Kgs')
    vehicle_type = models.CharField(max_length=20, blank=True, null=True)
    year_of_manufacture = models.CharField(max_length=20, blank=True, null=True)
    seating_capacity = models.CharField(max_length=20, blank=True, null=True)
    engine_capacity = models.CharField(max_length=20, blank=True, null=True)
    goods_description = models.TextField()
    country_of_origin= models.CharField(max_length=10, blank=True, null=True)
    converted_cif = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    import_duty = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    withholding_tax = models.DecimalField(max_digits=10, decimal_places=2)
    infrastructure_levy = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    environmental_levy = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    registration_fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stamp_duty = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    form_fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10)
    calculated_at = models.DateTimeField(auto_now_add=True)  # Timestamp field

    def __str__(self):
        return f"Tax Calculation for CIF: {self.cif} at {self.calculated_at}"

class HSCodes(models.Model):
    heading = models.CharField(max_length=10, blank=True, null=True)
    hs_code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField()
    unit_of_quantity = models.CharField(max_length=10, blank=True, null=True)
    rate = models.CharField(max_length=10, blank=True, null=True)

    def HSCodeRate(self):
        try:
            rate_as_float = float(self.rate)
            return f'{int(rate_as_float * 100)}%'
        except (ValueError, TypeError):
            return '' 
    
    def __str__(self):
        return str(self.description)

class MotorVehicleValueGuide(models.Model):
    HSCode = models.CharField(max_length=255)
    CountryOfOrigin = models.CharField(max_length=255)
    Description = models.TextField()
    YearOfManufacture = models.CharField(max_length=10, blank=True, null=True)
    Engine = models.CharField(max_length=10, blank=True, null=True)
    CIF = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.Description

class Blog(models.Model):
    blog_image = models.ImageField(upload_to="Blog_images", default="Blog_images/blog.jpg")
    blog_title = models.CharField(max_length=255, verbose_name='Blog Title')
    blog_author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='blogs', db_index=True)
    blog_category = models.CharField(max_length=255, verbose_name='Blog Category')
    blog_body_introduction = models.TextField(verbose_name='Introduction')
    blog_body_main = models.TextField(verbose_name='Main Content')
    blog_body_conclusion = models.TextField(verbose_name='Conclusion')
    blog_created_at = models.DateTimeField(auto_now_add=True)
    blog_updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Delete the old image when a new one is uploaded
        try:
            this = Blog.objects.get(id=self.id)
            if this.blog_image != self.blog_image:
                this.blog_image.delete(save=False)
        except Blog.DoesNotExist:
            pass
        
        super(Blog, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the associated image when a blog is deleted
        self.blog_image.delete(save=False)
        super(Blog, self).delete(*args, **kwargs)

    def __str__(self):
        """String representation of the Blog model."""
        return self.blog_title

    @property
    def date(self):
        """Get the date portion of blog_created_at."""
        return self.blog_created_at.date()

class BlogComment(models.Model):
    comment_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', db_index=True)
    comment_author = models.CharField(max_length=255, verbose_name='Author')
    comment_email = models.EmailField(validators=[EmailValidator()])
    comment_body = models.TextField(verbose_name='Comment Body')
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the Comment model."""
        return self.comment_author

    @property
    def date(self):
        """Get the date portion of comment_created_at."""
        return self.comment_created_at.date()
