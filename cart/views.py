from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from cart.cart import Cart
from cart.forms import CartAddForm
from coupons.forms import CouponApplyForm

from shop.models import Product
from shop.recommender import Recommender

@require_POST
def create_cart(request, product_id):
    """View to add product to the cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, **cd)
    return redirect('cart:cart_detail')


@require_POST
def remove_cart(request, product_id):
    """View to remove the product from the cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def detail(request):
    """View to display the cart detail"""
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddForm(initial={
            'quantity': item['quantity'],
            'override': True})
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    recommended_products = r.suggest_products_for(cart_products,4)
    return render(request, 'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form,
                   'recommended_products': recommended_products})
