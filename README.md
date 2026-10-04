# proyecto_shop

Tienda online minimalista hecha con Django, como proyecto del bootcamp ConquerBlocks.

E-commerce básico: catálogo de productos, carrito con sesión y creación de
pedidos. **Sin pasarela de pago real** — los pedidos quedan en estado pendiente.

## Stack

- Django 6.1 · Python 3.13
- SQLite en local · PostgreSQL en producción
- Tailwind CSS 4 + daisyUI 5 (build con pnpm)
- whitenoise (estáticos) · gunicorn (servidor WSGI)

## Apps

| App | Qué contiene |
|-----|--------------|
| `accounts` | `CustomUser` (extiende `AbstractUser`) + admin y forms propios |
| `catalog` | `Category` y `Product`, catálogo público y detalle |
| `orders` | `Order`, `OrderItem`, carrito de sesión y checkout |
| `home` | Landing y shell de templates |

## Puesta en marcha

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata categories products
python manage.py createsuperuser
python manage.py runserver
```

Los fixtures traen 4 categorías y 15 productos de ejemplo. Hay que cargarlos en
este orden: `Product.category` es obligatoria, así que la categoría debe existir
antes que el producto.

### CSS

`static/css/src/output.css` está commiteado, así que no hace falta compilar para
ver la app con estilos. Si cambias clases en los templates:

```bash
pnpm watch:css
```

## Variables de entorno

Se leen de `.env` en local (ver `.env.example`) y del panel de Render en producción.

| Variable | Para qué |
|----------|----------|
| `SECRET_KEY` | Firma de cookies y sesiones. **Obligatoria** |
| `DEBUG` | `True` en local, `False` en producción |
| `ALLOWED_HOSTS` | Dominios permitidos, separados por coma |
| `DATABASE_URL` | Si no está, se usa SQLite local |

## Producción (Render)

- **Build:** `pip install -r requirements.txt && python manage.py migrate && python manage.py loaddata categories products && python manage.py collectstatic --noinput`
- **Start:** `gunicorn config.wsgi`
- **Health check:** `/products/`

## Notas

- El carrito vive en la sesión (`request.session["cart"]`), no en la base de datos.
  Al confirmar se crea el `Order` con sus `OrderItem` y la sesión se vacía.
- `OrderItem.unit_price` y `Order.total` se congelan al confirmar el pedido, así
  que cambiar un precio no altera pedidos ya confirmados.
- El inventario se descuenta dentro del `filter(inventory__gte=quantity)` para que
  dos pedidos simultáneos no puedan solderse el mismo producto, y hay una
  `CheckConstraint` que impide que quede negativo.
