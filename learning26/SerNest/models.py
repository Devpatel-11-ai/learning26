from django.db import models
from django.contrib.auth.models import User


# -----------------------
# Admin
# -----------------------
class AdminProfile(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=15)
    role = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.admin.username


# -----------------------
# User
# -----------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


# -----------------------
# Service Category (Admin → Category = 1:M)
# -----------------------
class ServiceCategory(models.Model):
    admin = models.ForeignKey(AdminProfile, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


# -----------------------
# Service (Category → Service = 1:M)
# -----------------------
class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=150)
    description = models.TextField()
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.service_name


# -----------------------
# Service Provider
# -----------------------
class ServiceProvider(models.Model):
    provider_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    service_area = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    verification_status = models.BooleanField(default=False)
    availability = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.provider_name


# -----------------------
# Offer (Admin → Offer = 1:M)
# -----------------------
class Offer(models.Model):
    admin = models.ForeignKey(AdminProfile, on_delete=models.CASCADE)
    offer_name = models.CharField(max_length=150)
    discount_percentage = models.IntegerField()
    valid_from = models.DateField()
    valid_to = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.offer_name


# -----------------------
# Booking (User, Service, Provider = M:1)
# -----------------------
class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField()
    time_slot = models.CharField(max_length=50)
    booking_status = models.CharField(max_length=20)
    payment_mode = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking {self.id}"


# -----------------------
# Payment (Booking → Payment = 1:1)
# -----------------------
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id}"


# -----------------------
# Review (User → Review, Provider → Review = 1:M)
# -----------------------
class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Review {self.id}"


# -----------------------
# Complaint (Booking → Complaint = 1:M)
# -----------------------
class Complaint(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint {self.id}"


# -----------------------
# Subscription (Provider → Subscription = 1:M)
# -----------------------
class Subscription(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=20)
    commission_rate = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.provider} - {self.plan_type}"
