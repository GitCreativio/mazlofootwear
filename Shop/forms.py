from django import forms

class CheckoutForm(forms.Form):
    """
    Form for collecting user information during checkout.
    Includes fields for shipping address, city, state, zip code, and phone number.
    """
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter the full shipping address."
    )
    city = forms.CharField(
        max_length=100,
        help_text="Enter the city for the shipping address."
    )
    state = forms.CharField(
        max_length=100,
        help_text="Enter the state for the shipping address."
    )
    zip_code = forms.CharField(
        max_length=10,
        help_text="Enter the postal code for the shipping address."
    )
    phone_number = forms.CharField(
        max_length=15,
        help_text="Enter a contact phone number for delivery updates."
    )
