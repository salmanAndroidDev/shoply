from django import forms

PRODUCT_QUANTITY_CHOICE = [(i, str(i)) for i in range(1, 21)]


class CartAddForm(forms.Form):
    """Handy form to increase quantity of cart items"""
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICE,
                                      coerce=int)
    override = forms.BooleanField(required=False, initial=False,
                                  widget=forms.HiddenInput)
