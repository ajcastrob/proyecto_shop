from django.views.generic import ListView
from catalog.models import Product


class ProductListView(ListView):
    template_name = "products/products_list.html"
    model = Product
    context_object_name = "products"
