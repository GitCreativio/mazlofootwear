from django.db import models

# Create your models here.

class Stat(models.Model):
    """
    Model to represent a statistical fact or figure.

    Attributes:
        label (CharField): A descriptive label for the statistic (e.g., "Happy Customers").
        value (CharField): The corresponding numeric or textual value (e.g., "50,000+").
    """
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.value} {self.label}"
    

class Journey(models.Model):
    """
    Model to store the company’s journey or story section content.

    Attributes:
        title (CharField): Title heading for the journey section (default: "Our Journey").
        paragraph1 (TextField): First paragraph describing the journey.
        paragraph2 (TextField): Optional second paragraph with additional details.
        image (ImageField): Associated image illustrating the journey.
    """
    title = models.CharField(max_length=255, default="Our Journey")
    paragraph1 = models.TextField()
    paragraph2 = models.TextField(blank=True, null=True)    
    image = models.ImageField(upload_to='about_journey/')

    def __str__(self):
        return self.title  


class GreenPromiseItem(models.Model):
    """
    Model representing individual items of the 'Green Promise' sustainability commitments.

    Attributes:
        icon_class (CharField): Font Awesome icon CSS class for visual representation.
        title (CharField): Title of the green promise item.
        description (TextField): Detailed description of the promise.
        order (PositiveIntegerField): Position/order for display purposes.
    """
    icon_class = models.CharField(
        max_length=100,
        help_text='Font Awesome icon class, e.g. "fa-recycle"'
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Order of appearance")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    

class CoreValue(models.Model):
    """
    Model representing core values upheld by the company.

    Attributes:
        icon_class (CharField): Font Awesome icon CSS class for visual representation.
        title (CharField): Title of the core value.
        description (TextField): Explanation or details about the core value.
        order (PositiveIntegerField): Position/order for display purposes.
    """
    icon_class = models.CharField(
        max_length=100,
        help_text='Font Awesome icon class, e.g. "fa-award"'
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Order of appearance")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
