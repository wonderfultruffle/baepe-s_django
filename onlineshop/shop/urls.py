from django.urls import path
from .views import product_in_category, product_in_detail

urlpatterns = [
    path("", product_in_category, name="products_all"),
    path("<slug:category_slug>", product_in_category, name="products_in_category"),
    path("<int:id><slug:product_slug>", product_in_detail, name="product_detail"),
]