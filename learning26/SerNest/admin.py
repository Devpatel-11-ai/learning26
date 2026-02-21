from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import (
    User, ServiceCategory, Service,
    ServiceProvider, Subscription, Offer,
    Booking, Payment, Review, Complaint
)

# ===== ADMIN SITE BRANDING =====
admin.site.site_header = "SerNest Admin Panel"
admin.site.site_title  = "SerNest Admin"
admin.site.index_title = "Welcome to SerNest Management"


# ===== USER =====
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display   = ('username', 'email', 'phone', 'city', 'status', 'is_staff', 'date_joined')
    list_filter    = ('status', 'is_staff', 'is_active', 'city')
    search_fields  = ('username', 'email', 'phone', 'city')
    ordering       = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {
            'fields': ('phone', 'address', 'city', 'status')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {
            'fields': ('phone', 'address', 'city', 'status')
        }),
    )


# ===== SERVICE CATEGORY =====
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display  = ('icon', 'category_name', 'status', 'service_count')
    list_filter   = ('status',)
    search_fields = ('category_name',)
    list_editable = ('status',)

    def service_count(self, obj):
        count = obj.services.count()
        return format_html('<b style="color:#4f6ef7">{}</b> services', count)
    service_count.short_description = 'Total Services'


# ===== SERVICE =====
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ('service_name', 'category', 'min_price', 'max_price', 'availability')
    list_filter   = ('category', 'availability')
    search_fields = ('service_name', 'category__category_name')
    list_editable = ('availability',)


# ===== SERVICE PROVIDER =====
@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display    = (
        'provider_name', 'email', 'phone',
        'service_area', 'experience_years',
        'verification_badge', 'rating_stars', 'availability'
    )
    list_filter     = ('verification_status', 'availability', 'service_area')
    search_fields   = ('provider_name', 'email', 'phone', 'service_area')
    list_editable   = ('availability',)
    readonly_fields = ('rating',)
    filter_horizontal = ('services',)

    actions = ['verify_providers', 'reject_providers', 'block_providers']

    def verification_badge(self, obj):
        styles = {
            'verified': ('✅ Verified', '#28a745'),
            'pending':  ('⏳ Pending',  '#ffc107'),
            'rejected': ('❌ Rejected', '#dc3545'),
            'blocked':  ('🚫 Blocked',  '#6c757d'),
        }
        label, color = styles.get(obj.verification_status, ('?', '#000'))
        return format_html(
            '<span style="color:{};font-weight:600">{}</span>', color, label
        )
    verification_badge.short_description = 'Verification'

    def rating_stars(self, obj):
        return format_html(
            '<span style="color:#ffc107;font-weight:700">★ {}</span>', obj.rating
        )
    rating_stars.short_description = 'Rating'

    @admin.action(description='✅ Verify selected providers')
    def verify_providers(self, request, queryset):
        updated = queryset.update(verification_status='verified')
        self.message_user(request, f'✅ {updated} provider(s) verified.')

    @admin.action(description='❌ Reject selected providers')
    def reject_providers(self, request, queryset):
        updated = queryset.update(verification_status='rejected')
        self.message_user(request, f'❌ {updated} provider(s) rejected.')

    @admin.action(description='🚫 Block selected providers')
    def block_providers(self, request, queryset):
        updated = queryset.update(verification_status='blocked')
        self.message_user(request, f'🚫 {updated} provider(s) blocked.')


# ===== SUBSCRIPTION =====
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display  = ('provider', 'plan_badge', 'commission_rate', 'start_date', 'end_date')
    list_filter   = ('plan_type',)
    search_fields = ('provider__provider_name',)

    def plan_badge(self, obj):
        colors = {
            'basic':    '#6c757d',
            'standard': '#17a2b8',
            'premium':  '#ffc107',
        }
        color = colors.get(obj.plan_type, '#000')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 12px;'
            'border-radius:50px;font-size:0.8rem;font-weight:600">{}</span>',
            color, obj.plan_type.title()
        )
    plan_badge.short_description = 'Plan'


# ===== OFFER =====
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display  = ('offer_name', 'provider', 'discount_percentage', 'valid_from', 'valid_to', 'status_badge')
    list_filter   = ('status',)
    search_fields = ('offer_name', 'provider__provider_name')

    def status_badge(self, obj):
        colors = {
            'active':   '#28a745',
            'expired':  '#dc3545',
            'disabled': '#6c757d',
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 12px;'
            'border-radius:50px;font-size:0.8rem;font-weight:600">{}</span>',
            color, obj.status.title()
        )
    status_badge.short_description = 'Status'


# ===== BOOKING =====
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display    = (
        'id', 'user', 'provider', 'service',
        'booking_date', 'time_slot',
        'status_badge', 'payment_mode', 'total_amount', 'created_at'
    )
    list_filter     = ('booking_status', 'payment_mode', 'booking_date')
    search_fields   = ('user__username', 'provider__provider_name', 'service__service_name')
    readonly_fields = ('created_at',)
    date_hierarchy  = 'booking_date'

    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']

    def status_badge(self, obj):
        colors = {
            'pending':   '#ffc107',
            'confirmed': '#17a2b8',
            'completed': '#28a745',
            'rejected':  '#dc3545',
            'cancelled': '#6c757d',
        }
        color = colors.get(obj.booking_status, '#000')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 12px;'
            'border-radius:50px;font-size:0.8rem;font-weight:600">{}</span>',
            color, obj.booking_status.title()
        )
    status_badge.short_description = 'Status'

    @admin.action(description='✅ Mark as Confirmed')
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(booking_status='confirmed')
        self.message_user(request, f'✅ {updated} booking(s) confirmed.')

    @admin.action(description='🎉 Mark as Completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(booking_status='completed')
        self.message_user(request, f'🎉 {updated} booking(s) completed.')

    @admin.action(description='❌ Mark as Cancelled')
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(booking_status='cancelled')
        self.message_user(request, f'❌ {updated} booking(s) cancelled.')


# ===== PAYMENT =====
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display    = (
        'id', 'booking', 'amount',
        'payment_method', 'status_badge',
        'transaction_id', 'transaction_date'
    )
    list_filter     = ('payment_status', 'payment_method')
    search_fields   = ('transaction_id',)
    readonly_fields = ('transaction_date',)

    def status_badge(self, obj):
        colors = {
            'pending':  '#ffc107',
            'success':  '#28a745',
            'failed':   '#dc3545',
            'refunded': '#6c757d',
        }
        color = colors.get(obj.payment_status, '#000')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 12px;'
            'border-radius:50px;font-size:0.8rem;font-weight:600">{}</span>',
            color, obj.payment_status.title()
        )
    status_badge.short_description = 'Status'


# ===== REVIEW =====
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display    = ('user', 'provider', 'stars', 'review_date', 'status_badge')
    list_filter     = ('status', 'rating')
    search_fields   = ('user__username', 'provider__provider_name', 'review_text')
    readonly_fields = ('review_date',)

    actions = ['approve_reviews', 'remove_reviews']

    def stars(self, obj):
        filled = '★' * obj.rating
        empty  = '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color:#ffc107;font-size:1.1rem">{}</span>'
            '<span style="color:#ccc;font-size:1.1rem">{}</span>',
            filled, empty
        )
    stars.short_description = 'Rating'

    def status_badge(self, obj):
        colors = {
            'pending':  '#ffc107',
            'approved': '#28a745',
            'removed':  '#dc3545',
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 12px;'
            'border-radius:50px;font-size:0.8rem;font-weight:600">{}</span>',
            color, obj.status.title()
        )
    status_badge.short_description = 'Status'

    @admin.action(description='✅ Approve selected reviews')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'✅ {updated} review(s) approved.')

    @admin.action(description='🗑️ Remove selected reviews')
    def remove_reviews(self, request, queryset):
        updated = queryset.update(status='removed')
        self.message_user(request, f'🗑️ {updated} review(s) removed.')


# ===== COMPLAINT =====
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display    = (
        'id', 'user', 'issue_type',
        'status_badge', 'created_date', 'resolved_date'
    )
    list_filter     = ('status', 'issue_type')
    search_fields   = ('user__username', 'description', 'admin_notes')
    readonly_fields = ('created_date',)

    actions = ['mark_in_progress', 'mark_resolved', 'mark_closed']

    def status_badge(self, obj):
        colors = {
            'open':        '#dc3545',
            'in_progress': '#ffc107',
            'resolved':    '#28a745',
            'closed':      '#6c757d',
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 12px;'
            'border-radius:50px;font-size:0.8rem;font-weight:600">{}</span>',
            color, obj.status.replace('_', ' ').title()
        )
    status_badge.short_description = 'Status'

    @admin.action(description='🔄 Mark as In Progress')
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'🔄 {updated} complaint(s) marked as In Progress.')

    @admin.action(description='✅ Mark as Resolved')
    def mark_resolved(self, request, queryset):
        updated = queryset.update(status='resolved', resolved_date=timezone.now())
        self.message_user(request, f'✅ {updated} complaint(s) resolved.')

    @admin.action(description='🔒 Mark as Closed')
    def mark_closed(self, request, queryset):
        updated = queryset.update(status='closed', resolved_date=timezone.now())
        self.message_user(request, f'🔒 {updated} complaint(s) closed.')
