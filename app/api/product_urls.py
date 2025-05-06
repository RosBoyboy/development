from django.urls import path
from .product_views import ProductView, AddToCartView, ViewCartView, CheckoutView, UpdateCartView, RemoveCartView

urlpatterns = [
     path('', ProductView.as_view(), name='product_view'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/view/', ViewCartView.as_view(), name='view_cart'),
    path('cart/update/<int:item_id>/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/remove/<int:item_id>/', RemoveCartView.as_view(), name='remove_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]

