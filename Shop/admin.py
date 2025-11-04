from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.

class ColorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Color model.
    - Displays color information such as ID, name, code, and a color preview.
    - Enables searching by color name.
    """
    list_display = ('id', 'name', 'code', 'color_preview')    
    search_fields = ('name', )

    def color_preview(self, obj):
        """
        Provides a small color preview for the color in the admin panel.
        Displays a colored square based on the hex code of the color.
        """
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}"></div>',
            obj.code
        )
    color_preview.short_description = 'Preview'  # Sets the column header for the preview


class SizeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Size model.
    - Displays size information such as ID and code.
    - Enables filtering and searching by size code.
    """
    list_display = ('id', 'code')
    list_filter = ('code', )
    search_fields = ('code', )


class ProductImageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductImage model.
    - Displays product images and allows for sorting by product.
    - Includes a preview thumbnail for each image.
    """
    list_display = ('id', 'product', 'image_preview', 'image')
    list_filter = ('product',)

    def image_preview(self, obj):
        """
        Provides a thumbnail preview of the product image in the admin panel.
        Displays a small version of the image for better visual identification.
        """
        return format_html(
            '<img src="{}" style="width: 50px; height: 50px;" />',
            obj.image.url
        )
    image_preview.short_description = 'Image Preview'


class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    - Displays essential product details such as ID, name, description, price, and category.
    - Enables filtering by category and product type.
    - Provides search functionality for quick product lookup.
    """
    list_display = ('id', 'name', 'description', 'price', 'category', 'product_type', 'created_at')
    list_filter = ('category', 'product_type',)
    search_fields = ('name', 'description')
    ordering = ('name',)


class ProductVariantAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductVariant model.
    - Displays information about product variants such as color, size, stock, and price.
    - Enables filtering by product, color, and size.
    - Ensures that variants are listed in a logical order.
    """
    list_display = ('id', 'product', 'color', 'size', 'stock')
    list_filter = ('product', 'color', 'size')
    search_fields = ('product', 'color', 'size')
    ordering = ('product', 'color', 'size')


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
