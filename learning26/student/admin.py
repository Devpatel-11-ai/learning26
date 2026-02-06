from django.contrib import admin
from .models import Student,Product,StudentProfile,Category,Service,Booking,Payment,Order,Inventory
# Register your models here.

admin.site.register(Student)
admin.site.register(Product)
admin.site.register(StudentProfile)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Inventory)
