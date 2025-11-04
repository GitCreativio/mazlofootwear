from django.db import models

class HeroBanner(models.Model):
    """
    Model representing a hero banner section for the homepage or landing page.
    Contains an image, optional title, subtitle, and a clickable button with text and link.
    """
    image = models.ImageField(upload_to='hero_banners/')
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True, null=True)
    button_link = models.URLField(blank=True, null=True)

    def __str__(self):
        """
        String representation of the HeroBanner, returns the title if available,
        otherwise defaults to 'Hero Banner'.
        """
        return self.title or "Hero Banner"


class Category(models.Model):
    """
    Model representing product or content categories.
    Each category has a title, an optional image, a link URL, and an order number for sorting.
    """
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/', default='default_image.jpg', null=True, blank=True)
    link = models.URLField(default="#")  # Alternatively, can be a CharField for internal links
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        """
        String representation of the Category, returns its title.
        """
        return self.title


class NewArrivalBanner(models.Model):
    """
    Model representing banners for new arrivals or promotions.
    Includes title, subtitle (like price or tagline), image, and an optional button with text and link.
    """
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)  # e.g., price or tagline
    image = models.ImageField(upload_to='new_arrivals/')
    button_text = models.CharField(max_length=20, default='Quick View')
    button_link = models.URLField(blank=True, null=True)

    def __str__(self):
        """
        String representation of the NewArrivalBanner, returns its title.
        """
        return self.title


class FeaturedCollection(models.Model):
    """
    Model representing featured collections that may include images or videos.
    Each collection has a title, optional description, media file, and category label.
    Tracks creation date for ordering.
    """
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    media = models.FileField(upload_to='collections/')
    is_video = models.BooleanField(default=False)
    category = models.CharField(max_length=50, default='urban')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the FeaturedCollection, returns its title.
        """
        return self.title        


class StyleJournal(models.Model):
    """
    Model representing style journal entries or blog posts.
    Contains title, detailed description, associated image, and creation timestamp.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='journal/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the StyleJournal, returns its title.
        """
        return self.title
