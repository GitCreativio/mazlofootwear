from django.contrib import admin
from .models import Category, NewArrivalBanner, FeaturedCollection, HeroBanner, StyleJournal 

# Register your models here.

class HeroBannerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the HeroBanner model.
    Displays the id, title, subtitle, image, button text, and button link in the admin list view.
    """
    list_display = ('id', 'title', 'subtitle', 'image', 'button_text', 'button_link')   

class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    Displays the id, title, image, and link in the admin list view.
    """
    list_display = ('id', 'title', 'image', 'link')

class NewArrivalBannerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the NewArrivalBanner model.
    Displays the id, title, subtitle, image, button text, and button link in the admin list view.
    """
    list_display = ('id', 'title', 'subtitle', 'image', 'button_text', 'button_link')    

class FeaturedCollectionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the FeaturedCollection model.
    Displays the id, description, title, media, and category in the admin list view.
    """
    list_display = ('id', 'description', 'title', 'media', 'category')    

class StyleJournalAdmin(admin.ModelAdmin):
    """
    Admin configuration for the StyleJournal model.
    Displays the id, title, description, image, and creation date in the admin list view.
    """
    list_display = ('id', 'title', 'description', 'image', 'created_at')    

# Register models with their respective admin classes
admin.site.register(HeroBanner, HeroBannerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NewArrivalBanner, NewArrivalBannerAdmin)
admin.site.register(FeaturedCollection, FeaturedCollectionAdmin)
admin.site.register(StyleJournal, StyleJournalAdmin)
