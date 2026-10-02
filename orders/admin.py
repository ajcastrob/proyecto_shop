from django.contrib import admin
from orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "place_at", "payment_status"]
    list_filter = ["payment_status"]
    list_select_related = ["customer"]
    search_fields = ["customer__username", "customer__email"]
    list_per_page = 10
    date_hierarchy = "place_at"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "unit_price"]
    list_select_related = ["order", "product"]
    list_per_page = 10
