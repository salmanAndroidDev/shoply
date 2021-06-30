from django.contrib import admin
from coupons.models import Coupon


def discount_percent(obj):
    return f"{obj.discount}%"


discount_percent.short_description = 'discount'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """
    Custom Admin panel for Coupon model
    """
    list_display = ['code', 'valid_from', 'valid_to', discount_percent, 'active']
    list_filter = ('active', 'valid_from', 'valid_to')
    search_fields = ('code',)
