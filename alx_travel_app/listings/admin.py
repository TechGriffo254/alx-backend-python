from django.contrib import admin
from .models import Listing, Booking


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'location', 'price_per_night', 'available', 'host', 'created_at']
    list_filter = ['property_type', 'available', 'created_at']
    search_fields = ['title', 'description', 'location', 'address']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'property_type', 'host')
        }),
        ('Pricing & Availability', {
            'fields': ('price_per_night', 'available')
        }),
        ('Location', {
            'fields': ('location', 'address')
        }),
        ('Capacity', {
            'fields': ('bedrooms', 'bathrooms', 'max_guests')
        }),
        ('Amenities', {
            'fields': ('amenities',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'listing', 'guest', 'check_in_date', 'check_out_date', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'check_in_date', 'created_at']
    search_fields = ['listing__title', 'guest__username', 'guest__email']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
    fieldsets = (
        ('Booking Details', {
            'fields': ('listing', 'guest', 'status')
        }),
        ('Dates & Guests', {
            'fields': ('check_in_date', 'check_out_date', 'number_of_guests')
        }),
        ('Pricing', {
            'fields': ('total_price',)
        }),
        ('Additional Information', {
            'fields': ('special_requests',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
