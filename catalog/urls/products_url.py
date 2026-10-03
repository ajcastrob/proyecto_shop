from ..views import ProductListView
from django.urls import path

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
]
