from django.urls import path
from ..views import cart_add, cart_detail, cart_remove, cart_substract

app_name = "orders"

urlpatterns = [
    path("", cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", cart_add, name="cart_add"),
    path("substract/<int:product_id>/", cart_substract, name="cart_substract"),
    path("remove/<int:product_id>/", cart_remove, name="cart_remove"),
]
