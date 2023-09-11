from django.urls import path
from .views import product_in_category, product_in_detail

app_name = "shop"

urlpatterns = [
    path("", product_in_category, name="product_all"),
    path("<slug:category_slug>/", product_in_category, name="product_in_category"),
    path("<int:id>/<slug:product_slug>/", product_in_detail, name="product_detail"),
]