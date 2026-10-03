from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from catalog.models import Product

CART_SESSION_KEY = "cart"


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get(CART_SESSION_KEY, {})
    key = str(product.pk)
    cart[key] = cart.get(key, 0) + 1
    request.session[CART_SESSION_KEY] = cart
    return redirect(request.POST.get("next") or "orders:cart_detail")


def cart_detail(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    products = Product.objects.filter(pk__in=cart.keys())

    # El subtotal se calcula aquí, no en el template: Decimal * int es exacto
    # y en el template haría falta un filtro que no valida tipos.
    lines = [
        {
            "product": product,
            "quantity": cart[str(product.pk)],
            "subtotal": product.price * cart[str(product.pk)],
        }
        for product in products
    ]
    total = sum(line["subtotal"] for line in lines)

    return render(
        request,
        "cart/cart.html",
        {"lines": lines, "total": total},
    )


@require_POST
def cart_remove(request, product_id):
    cart = request.session.get(CART_SESSION_KEY, {})
    cart.pop(str(product_id), None)
    request.session[CART_SESSION_KEY] = cart
    return redirect("orders:cart_detail")
