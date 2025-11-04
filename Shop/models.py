from django.db import models
from django.core.validators import RegexValidator

# Color model: stores available color options.
class Color(models.Model):
    """
    Model representing a color option.
    Stores hex color code and a descriptive name.
    """
    hex_validator = RegexValidator(
        regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
        message='Enter a valid hex color code (e.g. #RRGGBB or #RGB)'
    )

    code = models.CharField(
        max_length=7,
        unique=True,
        validators=[hex_validator],
        help_text="Enter color in hexadecimal format (e.g. #FF0000 for red)"
    )
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Enter a descriptive name for the color"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name']

# Size model: stores available size options.
class Size(models.Model):
    """
    Model representing a shoe size.
    Stores size options in numerical format.
    """
    SIZE_CHOICES = [
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
        # Add more sizes as needed
    ]
    
    code = models.IntegerField(
        choices=SIZE_CHOICES,
        unique=True,
        help_text="Select numerical shoe size"
    )

    def __str__(self):
        return f"Size {self.get_code_display()}"

    class Meta:
        ordering = ['code']

# Product model: stores information about each product.
class Product(models.Model):
    """
    Model representing a product.
    Includes name, description, price, category, and type of product.
    """
    CATEGORY_CHOICES = [
        ('MEN', 'Men\'s'),
        ('WOMEN', 'Women\'s'),
        ('KIDS', 'Kids\''),
    ]
    
    TYPE_CHOICES = [
        ('SNEAKERS', 'Sneakers'),
        ('BOOTS', 'Boots'),
        ('SANDALS', 'Sandals'),
        ('FLATSHOES', 'Flat Shoes'),
        ('CASUALSHOES', 'Casual Shoes'),
        ('SLIPER AND FLIP FLOPS', 'Slipper and Flip Flops'),
        ('UNIFORMSHOES', 'Uniform Shoes'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(
        default="""
        - Style & Design: Classic slip-on chappal with a sleek, minimalist silhouette—perfect for casual and semi-formal wear.
        - Materials: Genuine leather upper with a soft, breathable lining; durable rubber outsole for superior grip.
        - Comfort: Cushioned footbed with arch support helps reduce fatigue; lightweight construction for all-day wear.        
        - Care: Wipe clean with a damp cloth; condition leather periodically to maintain finish.
        """.strip()
        )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    product_type = models.CharField(max_length=25, choices=TYPE_CHOICES)                 
    created_at = models.DateTimeField(auto_now_add=True)        

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('productdetails', args=[str(self.id)])

# ProductImage model: stores images related to products.
class ProductImage(models.Model):
    """
    Model for product images.
    Each product can have multiple images displayed in a specific order.
    """
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    order = models.PositiveIntegerField(
        default=0,
        help_text="Numerical order for image display"
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return f"Image {self.order} for {self.product.name}"

# ProductVariant model: stores variations of products based on size and color.
class ProductVariant(models.Model):
    """
    Model representing a variant of a product.
    A variant is a unique combination of product, size, and color, with a specific stock count and price.
    """
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='variants'
    )
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=10)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    class Meta:
        unique_together = ['product', 'color', 'size']  # Ensures unique combinations

    def __str__(self):
        return f"{self.product.name} - {self.color.name} - Size {self.size} (Stock: {self.stock})"
