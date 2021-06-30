from django.shortcuts import render, get_object_or_404
from .recommender import Recommender
from cart.forms import CartAddForm
from shop.models import Category, Product


def product_list(request, category_slug=None):
    """View to return total products or by category_slug"""
    category = None
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    """product detail view"""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    form = CartAddForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request, 'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': form,
                   'recommended_products': recommended_products})
