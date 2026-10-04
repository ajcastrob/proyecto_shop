from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import TemplateView

from catalog.models import Product
from orders.models import Order, OrderItem
from orders.views.orders_views import CART_SESSION_KEY


class OrderCheckoutView(TemplateView):
    template_name = "orders/checkout.html"
    model = Order

    def get_cart_data(self):
        cart = self.request.session.get(CART_SESSION_KEY, {})
        products = Product.objects.filter(pk__in=cart.keys())
        lines = [
            {
                "product": product,
                "quantity": cart[str(product.pk)],
                "subtotal": product.price * cart[str(product.pk)],
            }
            for product in products
        ]
        return lines, sum(line["subtotal"] for line in lines)

    def get(self, request, *args, **kwargs):
        lines, total = self.get_cart_data()
        if not lines:
            return redirect("orders:cart_detail")
        return self.render_to_response(self.get_context_data(lines=lines, total=total))

    def post(self, request, *args, **kwargs):
        lines, total = self.get_cart_data()
        if not lines:
            return redirect("orders:cart_detail")

        with transaction.atomic():
            order = Order.objects.create(customer=None)
            OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=order,
                        product=line["product"],
                        quantity=line["quantity"],
                        unit_price=line["product"].price,
                    )
                    for line in lines
                ]
            )

        request.session[CART_SESSION_KEY] = {}
        messages.success(request, f"Pedido #{order.pk} confirmado.")
        return redirect("orders:cart_detail")
