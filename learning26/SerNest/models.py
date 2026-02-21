from django.db import models
from django.contrib.auth.models import AbstractUser


# ===== USER =====
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('banned', 'Banned'),
    ], default='active')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='sernest_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='sernest_users',
        blank=True
    )

    def __str__(self):
        return self.username


# ===== SERVICE CATEGORY =====
class ServiceCategory(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], default='active')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Service Categories"


# ===== SERVICE =====
class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name='services'
    )
    service_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.service_name


# ===== SERVICE PROVIDER =====
class ServiceProvider(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='provider_profile'
    )
    provider_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    service_area = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField(default=0)
    verification_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    ], default='pending')
    availability = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    services = models.ManyToManyField(Service, blank=True, related_name='providers')

    def __str__(self):
        return self.provider_name


# ===== SUBSCRIPTION =====
class Subscription(models.Model):
    provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, related_name='subscriptions'
    )
    plan_type = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ], default='basic')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.provider.provider_name} - {self.plan_type}"


# ===== OFFER =====
class Offer(models.Model):
    provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE,
        related_name='offers', null=True, blank=True
    )
    offer_name = models.CharField(max_length=150)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('disabled', 'Disabled'),
    ], default='active')

    def __str__(self):
        return self.offer_name


# ===== BOOKING =====
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, related_name='bookings'
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    offer = models.ForeignKey(
        Offer, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings'
    )
    booking_date = models.DateField()
    time_slot = models.TimeField()
    booking_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    payment_mode = models.CharField(max_length=10, choices=[
        ('online', 'Online'),
        ('cash', 'Cash'),
    ], default='cash')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']


# ===== PAYMENT =====
class Payment(models.Model):
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[
        ('online', 'Online Gateway'),
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Card'),
    ])
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ], default='pending')
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.payment_status}"


# ===== REVIEW =====
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, related_name='reviews'
    )
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='review', null=True, blank=True
    )
    rating = models.PositiveSmallIntegerField(choices=[
        (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'),
        (4, '4 Stars'), (5, '5 Stars'),
    ])
    review_text = models.TextField(blank=True)
    review_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('removed', 'Removed'),
    ], default='pending')

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}★"

    class Meta:
        ordering = ['-review_date']


# ===== COMPLAINT =====
class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE,
        related_name='complaints', null=True, blank=True
    )
    issue_type = models.CharField(max_length=50, choices=[
        ('service_quality', 'Service Quality'),
        ('no_show', 'Provider No-Show'),
        ('payment', 'Payment Issue'),
        ('behaviour', 'Provider Behaviour'),
        ('other', 'Other'),
    ])
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], default='open')
    created_date = models.DateTimeField(auto_now_add=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Complaint #{self.id} - {self.status}"

    class Meta:
        ordering = ['-created_date']