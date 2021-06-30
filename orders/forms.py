from django import forms
from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    """Order creation form"""
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city')
