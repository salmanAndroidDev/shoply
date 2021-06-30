from decimal import Decimal

from django.conf import settings

from coupons.models import Coupon
from shop.models import Product


class Cart:
    """Handy class to store cart data into session"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override=False):
        """Add a product to the cart"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Make django save current modified session into db"""
        self.session.modified = True

    def remove(self, product):
        """Remove product from the cart"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Cart generator function that adds product and total_price"""
        cart = self.cart.copy()
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = (item['price'] * item['quantity'])
            yield item

    def __len__(self):
        """Return total products on the cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Return total price of the cart"""
        return sum((item['quantity'] * Decimal(item['price'])) \
                   for item in self.cart.values())

    def clear(self):
        """Delete the current cart from teh session"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        """Return the current coupon specified in the session"""
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """Return the amount that should be reduced from the total price"""
        if self.coupon:
            total = self.get_total_price()
            return (self.coupon.discount / Decimal(100)) * total
        return Decimal(0)

    def get_total_price_after_discount(self):
        """Return total price after applying discount"""
        total = self.get_total_price()
        return total - self.get_discount()
