from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('detail', views.detail, name='cart_detail'),
    path('add/<int:product_id>/', views.create_cart, name='cart_add'),
    path('remove/<int:product_id>/', views.remove_cart, name='cart_remove'),
]
