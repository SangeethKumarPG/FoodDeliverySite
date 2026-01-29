from django.contrib import admin
from django.utils.html import format_html
from .models import Category, MenuItem, Cart, CartItem, Order, OrderItem, Review

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_amount', 'status', 'created_at', 'map_link')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'latitude', 'longitude', 'google_map_link', 'interactive_map')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'total_amount', 'created_at')
        }),
        ('Customer Details', {
            'fields': ('full_name', 'email', 'phone', 'address', 'city')
        }),
        ('Location Details', {
            'fields': ('latitude', 'longitude', 'google_map_link', 'interactive_map')
        }),
    )

    def interactive_map(self, obj):
        if obj.latitude and obj.longitude:
            # Note: Using {{s}} to escape the curly braces for format_html/format
            return format_html(
                '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />'
                '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'
                '<div id="admin-map" style="height: 300px; width: 100%; max-width: 600px; border-radius: 10px; border: 1px solid #ccc; margin-top:10px;"></div>'
                '<script>'
                '   (function() {{'
                '       var map = L.map("admin-map").setView([{}, {}], 15);'
                '       L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{'
                '           attribution: "&copy; OpenStreetMap contributors"'
                '       }}).addTo(map);'
                '       L.marker([{}, {}]).addTo(map).bindPopup("Delivery Location").openPopup();'
                '       setTimeout(function(){{ map.invalidateSize(); }}, 500);'
                '   }})();'
                '</script>',
                obj.latitude, obj.longitude, obj.latitude, obj.longitude
            )
        return "No location coordinates available"
    
    interactive_map.short_description = "Delivery Map"

    def google_map_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank" style="display:inline-block; padding:8px 15px; background-color:#4b5d1a; color:white; text-decoration:none; border-radius:5px;">Open in Google Maps</a>', url)
        return "No location set"

    def map_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank">📍 View Map</a>', url)
        return "No location"
    map_link.short_description = "Map"
    
    google_map_link.short_description = "Map Link"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

admin.site.register(Cart)
admin.site.register(CartItem)
