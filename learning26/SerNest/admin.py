from django.contrib import admin
from .models import AdminProfile, UserProfile, ServiceCategory, Service, ServiceProvider, Offer, Booking, Payment, Review, Complaint, Subscription

admin.site.register(AdminProfile)
admin.site.register(UserProfile)
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(ServiceProvider)
admin.site.register(Offer)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Complaint)
admin.site.register(Subscription)
