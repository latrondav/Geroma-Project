from django.contrib import admin
from GeromaApp.models import *

# Register your models here.
#admin.site.register(Contacts)
admin.site.register(Profile)
admin.site.register(Events)
admin.site.register(Blog)
admin.site.register(BlogComment)
admin.site.register(Alumni_Carbinets)
admin.site.register(TaxCalculation)

@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'contact_email',)
    ordering = ('contact_name',)
    search_fields = ('contact_name', 'contact_email',)

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_name', 'order_course', 'order_yos',)
    ordering = ('order_name',)
    search_fields = ('order_name', 'order_course', 'order_yos',)
