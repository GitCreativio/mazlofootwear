from django import forms
from .models import Return

class CheckoutForm(forms.Form):
    """
    Form used during the checkout process to collect shipping details.
    """
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter the full shipping address."
    )
    city = forms.CharField(
        max_length=100,
        help_text="City for delivery."
    )
    state = forms.CharField(
        max_length=100,
        help_text="State for delivery."
    )
    zip_code = forms.CharField(
        max_length=10,
        help_text="Postal/ZIP code."
    )
    phone_number = forms.CharField(
        max_length=15,
        help_text="Recipient's contact phone number."
    )


class ReturnForm(forms.ModelForm):
    """
    Form for users to submit a return request for an order.
    """
    class Meta:
        model = Return
        fields = ['reason', 'description']
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Please provide details about your return request'
                }
            ),
        }
