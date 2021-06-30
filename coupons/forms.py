from django import forms


class CouponApplyForm(forms.Form):
    """
    Form to apply coupon to the order
    """
    code = forms.CharField(max_length=50)