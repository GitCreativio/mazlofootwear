from django.contrib import admin
from .models import *

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Cart model.
    Displays and filters user cart items, disallowing manual additions from the admin panel.
    """
    list_display = ('id', 'user', 'variant', 'quantity', 'created_at')
    list_filter = ('user', 'created_at')

    def has_add_permission(self, request, obj=None):
        """
        Disables the ability to add a cart item manually from the admin interface.
        """
        return False


class orderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Order model.
    Displays key order details and filters by various fields, disallowing manual additions.
    """
    list_display = ('id', 'user', 'shipping_address', 'city', 'total_amount', 'order_status', 'payment_method')
    list_filter = ('id', 'user', 'city', 'order_status')

    def has_add_permission(self, request, obj=None):
        """
        Disables the ability to add an order manually from the admin interface.
        """
        return False


class orderiteamAdmin(admin.ModelAdmin):
    """
    Admin configuration for the OrderItem model.
    Displays individual order item details and filters by related fields.
    """
    list_display = ('id', 'order', 'variant', 'quantity', 'price')
    list_filter = ('id', 'order', 'variant')

    def has_add_permission(self, request, obj=None):
        """
        Disables the ability to add an order item manually from the admin interface.
        """
        return False


class ReturnAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Return model.
    Displays return requests with filtering options and restricts manual additions.
    """
    list_display = ('id', 'order', 'user', 'reason', 'created_at')
    list_filter = ('order', 'user', 'reason', 'created_at')

    def has_add_permission(self, request, obj=None):
        """
        Disables the ability to add a return manually from the admin interface.
        """
        return False


# Registering models to the admin interface
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, orderAdmin)
admin.site.register(OrderItem, orderiteamAdmin)
admin.site.register(Return, ReturnAdmin)
