from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib import messages
from catalog.models import Product

CART_SESSION_KEY = "cart"


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # El detalle bloquea el boton si inventory == 0, pero esta vista se
    # puede llamar directamente. Se comprueba aqui tambien.
    if product.inventory <= 0:
        messages.error(request, f"'{product.title}' está agotado.")
        return redirect(request.POST.get("next") or "orders:cart_detail")

    cart = request.session.get(CART_SESSION_KEY, {})
    key = str(product.pk)
    cart[key] = cart.get(key, 0) + 1
    request.session[CART_SESSION_KEY] = cart
    return redirect(request.POST.get("next") or "orders:cart_detail")


@require_POST
def cart_substract(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get(CART_SESSION_KEY, {})
    key = str(product.pk)

    if key in cart:
        # Restar uno al contenido actual
        cart[key] -= 1

        # Si la cantidad llega a 0 o menos, eliminar el producto del carrito
        if cart[key] <= 0:
            del cart[key]
        # Guardar los cambios en la sesión.
        request.session[CART_SESSION_KEY] = cart
    return redirect(request.POST.get("next") or "orders:cart_detail")


def cart_detail(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    products = Product.objects.filter(pk__in=cart.keys())

    # El subtotal se calcula aquí, no en el template: Decimal * int es exacto
    # y en el template haría falta un filtro que no valida tipos.
    lines = []
    for product in products:
        lines.append(
            {
                "product": product,
                "quantity": cart[str(product.pk)],
                "subtotal": product.price * cart[str(product.pk)],
            }
        )
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
