from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path("", home, name='home'),  # Home page
    path("menu/", Menu, name='menu'),  # Menu page
    path('category/<str:url>/', category, name='category'),  # Category page
    path('category/', Hover, name='hover'),  # Hover category
    path('product/<str:product_url>/', product_detail, name='product_detail'),  # Product detail page
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),  # Add to cart
    path('send_mail/', sendMail, name='mail'),  # Send mail after checkout
    path('update-cart/<int:item_id>/', update_cart, name='update_cart'),  # Update cart item
    path('delete-cart/<int:item_id>/', delete_cart, name='delete_cart'),  # Delete cart item
    path('checkout/', checkout, name='checkout'),  # Checkout page (missing in original code)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
