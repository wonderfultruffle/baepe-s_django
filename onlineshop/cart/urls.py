from django.urls import path

from .views import add, remove, detail

urlpattern = [
    path("", detail, name="detail"),
    path("add/<int:product_id>", add, name="product_add"),
    path("remove/<int:product_id>", remove, name="product_remove"),
]