from django.views.generic import ListView, DetailView
from catalog.models import Product


class ProductListView(ListView):
    template_name = "products/products_list.html"
    model = Product
    context_object_name = "products"


class ProductDetailView(DetailView):
    template_name = "products/products_details.html"
    model = Product
    context_object_name = "product"
