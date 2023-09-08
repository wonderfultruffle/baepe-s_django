from django.urls import path
from .views import products_in_category, product_in_detail

urlpatterns = [
    path("", products_in_category, name="product_all"),
    path("<slug:category_slug>", products_in_category, name="products_in_category"),
    path("<id:id><slug:product_slug>", product_in_detail, name="product_detail"),
]