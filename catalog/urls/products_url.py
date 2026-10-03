from ..views import ProductListView, ProductDetailView
from django.urls import path

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("details/<pk>/", ProductDetailView.as_view(), name="detail"),
]
