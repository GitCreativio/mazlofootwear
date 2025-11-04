from django.db import models
from Shop.models import (
    Product,
    ProductVariant
)
from django.contrib.auth.models import User

# Create your models here.

class Cart(models.Model):
    """
    Represents an item in a user's shopping cart.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user who owns the cart.")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, default=1, help_text="The specific product variant added to the cart.")
    quantity = models.PositiveIntegerField(default=1, help_text="Number of units of the product variant.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the cart item was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the cart item was last updated.")

    @property
    def total_price(self):
        """
        Calculates the total price for this cart item.
        """
        return self.quantity * self.variant.price

    def __str__(self):
        return f"{self.quantity}x {self.variant} ({self.user})"


class Order(models.Model):
    """
    Stores details of an order placed by a user.
    """
    OrderStatus = (
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
    )

    PaymentStatus = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user who placed the order.")
    order_date = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the order was created.")
    shipping_address = models.TextField(help_text="Shipping address for the order.")
    city = models.CharField(max_length=100, help_text="City for delivery.")
    state = models.CharField(max_length=100, help_text="State for delivery.")
    zip_code = models.CharField(max_length=10, help_text="ZIP code for delivery.")
    phone_number = models.CharField(max_length=15, help_text="Contact phone number.")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total amount of the order.")
    payment_method = models.CharField(max_length=50, default='COD', help_text="Payment method used (e.g., COD, Card).")
    payment_status = models.CharField(max_length=20, choices=PaymentStatus, default='Pending', help_text="Status of the payment.")
    order_status = models.CharField(max_length=20, choices=OrderStatus, default='Processing', help_text="Current status of the order.")

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    """
    Represents an individual item in an order.
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, help_text="The order to which this item belongs.")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, default=1, help_text="The product variant ordered.")
    quantity = models.PositiveIntegerField(help_text="Quantity of the product variant.")
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price of the product at the time of ordering.")

    @property
    def total_price(self):
        """
        Calculates the total price for this order item.
        """
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.variant.product.name}"


class Return(models.Model):
    """
    Manages product return requests made by users.
    """
    RETURN_REASONS = (
        ('wrong_size', 'Wrong Size'),
        ('damaged', 'Product Damaged'),
        ('not_as_described', 'Not As Described'),
        ('defective', 'Defective Product'),
        ('changed_mind', 'Changed Mind'),
        ('other', 'Other'),
    )

    RETURN_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, help_text="The order being returned.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user requesting the return.")
    reason = models.CharField(max_length=50, choices=RETURN_REASONS, help_text="Reason for return.")
    description = models.TextField(help_text="Detailed description for the return request.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the return request was created.")
    status = models.CharField(max_length=20, choices=RETURN_STATUS, default='pending', help_text="Status of the return request.")

    def __str__(self):
        return f"Return for Order #{self.order.id} - {self.user.username}"
