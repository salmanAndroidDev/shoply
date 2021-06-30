from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from shop.models import Product


class Order(models.Model):
    """Order model to save customer info"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)

    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[
                                       MinValueValidator(0),
                                       MaxValueValidator(100)
                                   ])

    class Meta:
        ordering = ('-created',)

    def get_total_cost(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total - ((self.discount / Decimal(100)) * total)

    def __str__(self):
        return f"{self.first_name} {self.last_name} from {self.city}"


class OrderItem(models.Model):
    """OrderItem model, Items of the order"""
    order = models.ForeignKey('Order',
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}"
