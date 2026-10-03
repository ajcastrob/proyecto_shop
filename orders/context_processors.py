from orders.views.orders_views import CART_SESSION_KEY


def cart(request):
    """Expone el carrito y su contador a todos los templates.

    El carrito vive en orders, asi que es orders quien lo publica. El
    contador se calcula aqui porque en el template no hay filtro para
    sumar los valores de un dict.
    """
    cart = request.session.get(CART_SESSION_KEY, {})
    return {
        "cart": cart,
        "cart_count": sum(cart.values()),
    }
