from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from catalog.models import Category, Product


class ProductListView(ListView):
    template_name = "products/products_list.html"
    model = Product
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        # El filtro va por query param (?category=<pk>) para poder combinarlo
        # con otros filtros mas adelante sin crear una vista por combinacion.
        # Se valida que sea un entero antes de filtrar: un category=abc lanza
        # ValueError dentro del ORM (500) y eso no debe ser un 500.
        pk = self.request.GET.get("category", "").strip()
        if pk:
            if not pk.isdigit():
                raise Http404("Categoría no encontrada")
            self.category = get_object_or_404(Category, pk=pk)
            queryset = queryset.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = getattr(self, "category", None)
        context["categories"] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    template_name = "products/products_details.html"
    model = Product
    context_object_name = "product"
