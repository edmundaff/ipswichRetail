from django import forms
from .models import Order


class DemoCheckoutForm(forms.ModelForm):
    """No payment details or card information are accepted by this demo."""

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'address_line', 'city', 'postcode']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Alex Morgan', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'alex@example.com', 'autocomplete': 'email'}),
            'address_line': forms.TextInput(attrs={'placeholder': '12 Example Street', 'autocomplete': 'street-address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Ipswich', 'autocomplete': 'address-level2'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'IP1 1AA', 'autocomplete': 'postal-code'}),
        }

    def clean_postcode(self):
        postcode = self.cleaned_data['postcode'].strip().upper()
        if len(postcode) < 5:
            raise forms.ValidationError('Please enter a valid postcode.')
        return postcode
