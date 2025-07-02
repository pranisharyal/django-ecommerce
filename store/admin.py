from django.contrib import admin
from .models import Order, OrderItem, Product, Category

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    list_filter = ['category']
    search_fields = ['name']

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# Inline Order Items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'quantity', 'price']
    extra = 0
    classes = ['collapse']

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'status', 'created_at']
    list_display_links = ['id', 'name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'total_price']
    inlines = [OrderItemInline]
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone']

    fieldsets = (
        ('Customer Info', {
            'fields': ('name', 'email', 'phone', 'address')
        }),
        ('Order Details', {
            'fields': ('status', 'total_price', 'created_at')
        }),
    )

# Custom Admin Titles
admin.site.site_header = "🛒 E-commerce Admin"
admin.site.site_title = "E-commerce Admin Portal"
admin.site.index_title = "Welcome to the E-commerce Dashboard"
