from django.contrib import admin
from .models import Stat, Journey, GreenPromiseItem, CoreValue

# Register your models here.

class StatAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Stat model.

    Displays the ID, label, and value fields in the admin list view.
    """
    list_display = ['id', 'label', 'value']


class JourneyAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Journey model.

    Displays the ID, title, paragraphs, and image fields in the admin list view.
    """
    list_display = ['id', 'title', 'paragraph1', 'paragraph2', 'image']


class GreenPromiseItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the GreenPromiseItem model.

    Displays the ID, title, and description fields in the admin list view.
    """
    list_display = ['id', 'title', 'description']


class CoreValueAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CoreValue model.

    Displays the ID, title, description, and display order in the admin list view.
    """
    list_display = ['id', 'title', 'description', 'order']


# Registering models with the Django admin interface using their respective configurations.
admin.site.register(Stat, StatAdmin)
admin.site.register(Journey, JourneyAdmin)
admin.site.register(GreenPromiseItem, GreenPromiseItemAdmin)
admin.site.register(CoreValue, CoreValueAdmin)
